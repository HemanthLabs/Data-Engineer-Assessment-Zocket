from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook
from datetime import datetime, timedelta
import requests
import json
import psycopg2

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for Facebook Ads and Google Ads',
    schedule_interval=timedelta(days=1),
)

def fetch_facebook_ads_data():
    connection = BaseHook.get_connection('facebook_ads')
    headers = {
        'Authorization': f'Bearer {connection.password}',
    }
    url = 'https://graph.facebook.com/v12.0/me/ads'
    response = requests.get(url, headers=headers)
    data = response.json()
    with open('/tmp/facebook_ads_data.json', 'w') as f:
        json.dump(data, f)

def fetch_google_ads_data():
    connection = BaseHook.get_connection('google_ads')
    headers = {
        'Authorization': f'Bearer {connection.password}',
    }
    url = 'https://googleads.googleapis.com/v10/customers/1234567890/googleAds:searchStream'
    response = requests.post(url, headers=headers)
    data = response.json()
    with open('/tmp/google_ads_data.json', 'w') as f:
        json.dump(data, f)

def transform_data():
    # Transform Facebook Ads data
    with open('/tmp/facebook_ads_data.json') as f:
        facebook_ads_data = json.load(f)
    transformed_facebook_ads_data = [
        {
            'ad_id': ad['id'],
            'ad_name': ad['name'],
            'impressions': ad['impressions'],
            'clicks': ad['clicks'],
            'spend': ad['spend'],
        }
        for ad in facebook_ads_data['data']
    ]
    
    # Transform Google Ads data
    with open('/tmp/google_ads_data.json') as f:
        google_ads_data = json.load(f)
    transformed_google_ads_data = [
        {
            'campaign_id': campaign['id'],
            'campaign_name': campaign['name'],
            'impressions': campaign['metrics']['impressions'],
            'clicks': campaign['metrics']['clicks'],
            'cost_micros': campaign['metrics']['cost_micros'],
        }
        for campaign in google_ads_data['results']
    ]

    # Save transformed data
    with open('/tmp/transformed_facebook_ads_data.json', 'w') as f:
        json.dump(transformed_facebook_ads_data, f)
    with open('/tmp/transformed_google_ads_data.json', 'w') as f:
        json.dump(transformed_google_ads_data, f)

def load_data_to_rds():
    connection = BaseHook.get_connection('rds_postgres')
    conn = psycopg2.connect(
        host=connection.host,
        port=connection.port,
        user=connection.login,
        password=connection.password,
        dbname=connection.schema
    )
    cursor = conn.cursor()

    with open('/tmp/transformed_facebook_ads_data.json') as f:
        facebook_ads_data = json.load(f)
    for ad in facebook_ads_data:
        cursor.execute(
            """
            INSERT INTO facebook_ads (ad_id, ad_name, impressions, clicks, spend)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (ad['ad_id'], ad['ad_name'], ad['impressions'], ad['clicks'], ad['spend'])
        )

    with open('/tmp/transformed_google_ads_data.json') as f:
        google_ads_data = json.load(f)
    for campaign in google_ads_data:
        cursor.execute(
            """
            INSERT INTO google_ads (campaign_id, campaign_name, impressions, clicks, cost_micros)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (campaign['campaign_id'], campaign['campaign_name'], campaign['impressions'], campaign['clicks'], campaign['cost_micros'])
        )

    conn.commit()
    cursor.close()
    conn.close()

fetch_facebook_ads_task = PythonOperator(
    task_id='fetch_facebook_ads_data',
    python_callable=fetch_facebook_ads_data,
    dag=dag,
)

fetch_google_ads_task = PythonOperator(
    task_id='fetch_google_ads_data',
    python_callable=fetch_google_ads_data,
    dag=dag,
)

transform_data_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

load_data_to_rds_task = PythonOperator(
    task_id='load_data_to_rds',
    python_callable=load_data_to_rds,
    dag=dag,
)

fetch_facebook_ads_task >> fetch_google_ads_task >> transform_data_task >> load_data_to_rds_task
