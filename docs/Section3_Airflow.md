# Apache Airflow Overview

Apache Airflow is an open-source workflow management platform designed to automate and orchestrate complex data workflows and ETL processes. Developed by Airbnb, Airflow allows users to define workflows as code, ensuring better version control, scalability, and ease of use.

### Key Features of Apache Airflow:
- **Directed Acyclic Graphs (DAGs)**: Workflows are represented as DAGs, where each node is a task, and edges define the dependencies between tasks.
- **Scheduler**: The scheduler triggers tasks based on a defined schedule, handling dependencies and ensuring that tasks are executed in the correct order.
- **Extensibility**: Airflow is highly extensible, allowing users to define custom operators and hooks for various external systems.
- **UI**: Airflow comes with a rich user interface for visualizing DAGs, monitoring task execution, and managing workflows.
- **Scalability**: Airflow can be scaled horizontally to handle large workflows and can integrate with other distributed systems.

## How Apache Airflow Facilitates ETL Pipeline Orchestration

Apache Airflow simplifies the orchestration of ETL pipelines by providing a framework where each step of the ETL process can be defined as a task within a DAG. The following aspects highlight how Airflow facilitates ETL orchestration:

1. **Task Scheduling and Dependency Management**: Airflow's scheduler ensures that tasks are executed in the correct order based on dependencies. This is crucial for ETL processes where data extraction, transformation, and loading must happen sequentially or in a specific order.
2. **Retry Mechanism**: Airflow allows configuration for retries in case of task failures, ensuring robustness in the ETL process.
3. **Logging and Monitoring**: Airflow provides detailed logs and a user interface for monitoring task status, execution times, and failures, which helps in troubleshooting and maintaining ETL workflows.
4. **Integrations**: Airflow integrates with a wide range of services and databases through pre-built operators, enabling easy connections to data sources and destinations.
5. **Parallelism and Concurrency**: Airflow supports running tasks in parallel and managing concurrency, which is essential for handling large volumes of data efficiently.
6. **Code as Configuration**: Workflows are defined using Python code, making it easier to version control, test, and collaborate on ETL pipeline definitions.

## Example of an Airflow DAG for the ETL Process

Here is an example of an Airflow DAG that schedules and orchestrates the ETL process for extracting data from Facebook Ads and Google Ads, transforming it, and loading it into an RDS database:

```python
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

```

## Explanation of DAG 
### Data Extraction:
fetch_facebook_ads_data: Fetches data from the Facebook Ads API and saves it to a temporary JSON file.
fetch_google_ads_data: Fetches data from the Google Ads API and saves it to a temporary JSON file.

### Data Transformation:
transform_data: Reads the extracted data, processes it into a structured format suitable for storage, and saves the transformed data to temporary JSON files.

### Data Loading:
load_data_to_rds: Loads the transformed data into an RDS PostgreSQL database.

Each Python function is responsible for a distinct phase of the ETL process, ensuring modularity and clarity in the workflow.

