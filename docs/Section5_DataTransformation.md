# Transforming JSON Data for AWS Redshift

## Example JSON Data Sample

```json
[
    {
        "ad_id": "12345",
        "ad_name": "Sample Ad 1",
        "date_start": "2024-01-01",
        "date_stop": "2024-01-01",
        "impressions": "1000",
        "clicks": "100",
        "spend": "50.00"
    },
    {
        "ad_id": "67890",
        "ad_name": "Sample Ad 2",
        "date_start": "2024-01-01",
        "date_stop": "2024-01-01",
        "impressions": "1500",
        "clicks": "200",
        "spend": "75.00"
    }
]
```

## Transformation Function
The goal is to transform this JSON data into a structured format, such as a list of tuples, which can then be inserted into an AWS Redshift database. The Redshift table schema might look like this
```sql
CREATE TABLE facebook_ads (
    ad_id VARCHAR(50),
    ad_name VARCHAR(255),
    date_start DATE,
    date_stop DATE,
    impressions INTEGER,
    clicks INTEGER,
    spend DECIMAL(10, 2)
);
```

## Python Function for transformation
```python
import json
from datetime import datetime

def transform_facebook_ads(json_data):
    # Load JSON data
    ads_data = json.loads(json_data)
    
    # Initialize a list to hold the structured data
    structured_data = []
    
    # Iterate through each ad record in the JSON data
    for ad in ads_data:
        ad_id = ad.get("ad_id")
        ad_name = ad.get("ad_name")
        date_start = datetime.strptime(ad.get("date_start"), '%Y-%m-%d').date()
        date_stop = datetime.strptime(ad.get("date_stop"), '%Y-%m-%d').date()
        impressions = int(ad.get("impressions"))
        clicks = int(ad.get("clicks"))
        spend = float(ad.get("spend"))
        
        # Append the structured data as a tuple
        structured_data.append((ad_id, ad_name, date_start, date_stop, impressions, clicks, spend))
    
    return structured_data

# Example usage
json_data = '''[
    {
        "ad_id": "12345",
        "ad_name": "Sample Ad 1",
        "date_start": "2024-01-01",
        "date_stop": "2024-01-01",
        "impressions": "1000",
        "clicks": "100",
        "spend": "50.00"
    },
    {
        "ad_id": "67890",
        "ad_name": "Sample Ad 2",
        "date_start": "2024-01-01",
        "date_stop": "2024-01-01",
        "impressions": "1500",
        "clicks": "200",
        "spend": "75.00"
    }
]'''

transformed_data = transform_facebook_ads(json_data)
print(transformed_data)
```

## Loading Data into Redshift
After transforming the data, the next step is to load it into the AWS Redshift database. We can use the boto3 library to interact with Redshift. The following script demonstrates loading the transformed data into Redshift:

```python
import psycopg2
import boto3

# Function to load data into Redshift
def load_data_to_redshift(data, table_name):
    conn = psycopg2.connect(
        dbname='your_db',
        user='your_user',
        password='your_password',
        host='your_redshift_cluster',
        port='5439'
    )
    cursor = conn.cursor()
    
    for record in data:
        insert_query = f"""
        INSERT INTO {table_name} (ad_id, date_start, date_stop, impressions, clicks, spend, link_clicks, page_engagement)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, record)
    
    conn.commit()
    cursor.close()
    conn.close()

# Load the transformed data
load_data_to_redshift(transformed_data, 'facebook_ads')
```

## Explanation

1. **Loading JSON Data**: The `json.loads` function converts the JSON string into a Python list of dictionaries.
2. **Initializing a List for Structured Data**: The `structured_data` list will store the transformed data as tuples.
3. **Iterating Through Each Record**: The function loops through each ad record in the JSON data.
4. **Extracting and Converting Data**:
    - `ad_id` and `ad_name` are extracted directly from the JSON.
    - `date_start` and `date_stop` are converted to Python date objects using `datetime.strptime`.
    - `impressions` and `clicks` are converted to integers.
    - `spend` is converted to a float.
5. **Appending Structured Data**: Each transformed record is appended to `structured_data` as a tuple.
6. **Returning Structured Data**: The function returns the list of tuples, which can be easily inserted into a Redshift table.
