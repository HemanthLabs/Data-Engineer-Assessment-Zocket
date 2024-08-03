# ETL Pipeline Design

## High-Level ETL Pipeline Architecture

### Data Extraction

#### Facebook Ads
- **API**: Facebook Marketing API (Graph API)
- **Authentication**: OAuth 2.0
- **Endpoints**: 
  - `/act_{ad_account_id}/ads`
  - `/act_{ad_account_id}/adsets`
  - `/act_{ad_account_id}/campaigns`
- **Data Extraction Frequency**: Hourly to daily, based on campaign activity and reporting needs
- **Data**: Metrics like impressions, clicks, conversions, spend, ad performance details

#### Google Ads
- **API**: Google Ads API
- **Authentication**: OAuth 2.0
- **Endpoints**: `customers/{customerId}/googleAds:search`
- **Data Extraction Frequency**: Hourly to daily, synchronized with Facebook Ads extraction
- **Data**: Metrics such as clicks, impressions, cost, conversions, keyword performance

### Data Transformation
- **Normalization**: Convert data from both Facebook Ads and Google Ads into a standardized format
- **Date and Time**: Standardize to UTC
- **Metric Names**: Normalize metrics like clicks, impressions, and cost across both platforms

#### Cleaning
- **Duplicates**: Remove duplicate records
- **Missing Values**: Handle missing data appropriately (imputation or default values)
- **Data Types**: Ensure all fields are in the correct format (e.g., integers for clicks, decimals for cost)

#### Aggregation
- **Granularity**: Aggregate data to the required level (e.g., daily summaries, campaign-level data)
- **Summary**: Summarize metrics by campaign, ad set, and ad level

#### Mapping
- **Field Mapping**: Map fields from Facebook Ads and Google Ads data structures to a unified schema suitable for RDS
  - Facebook Ads `ad_id` -> RDS `ad_id`
  - Google Ads `ad_group_id` -> RDS `ad_group_id`

### Data Loading

#### RDS Database Schema
```sql
CREATE TABLE ad_data (
  ad_id VARCHAR(255) PRIMARY KEY,
  campaign_id VARCHAR(255),
  platform VARCHAR(50),
  clicks INT,
  impressions INT,
  cost DECIMAL(10, 2),
  date DATE
);
```

#### Loading Process
- Use batch inserts or bulk load operations for efficiency.
- Utilize transaction management to ensure data integrity during the load process.
- Schedule the load process after transformation is complete.

#### Error Handling

- **Extraction Errors**: Implement retries for API requests in case of network or server issues.
- **Transformation Errors**: Validate data types and handle transformation exceptions.
- **Loading Errors**: Use transactional inserts to roll back in case of failures to maintain data consistency.

### Monitoring and Alerts

- **Monitoring**:
  - Use monitoring tools like AWS CloudWatch to track API request metrics, extraction success rates, and load performance.
  - Implement detailed logging for each stage of the ETL process for debugging and auditing purposes.

- **Alerts**:
  - Set up alerts for failed API requests, transformation errors, and loading failures.
  - Integrate alerting with communication tools like Slack, email, or SMS for real-time notifications.

### Scalability

- **Horizontal Scaling**:
  - Distribute the extraction and transformation workload across multiple worker nodes to handle increased data volume.
  - Use a distributed computing framework like Apache Spark for large-scale data transformations.

- **Vertical Scaling**:
  - Optimize the RDS instance type and storage based on data volume and query performance.
  - Implement read replicas in RDS for high read throughput and load balancing.

- **Automation**:
  - Use Apache Airflow to orchestrate and schedule ETL tasks. Define Directed Acyclic Graphs (DAGs) to manage task dependencies and execution order.

### ETL Pipeline Services and Tools

#### Services Used

1. **Data Extraction**:
   - Facebook Ads API: For extracting ad performance data from Facebook.
   - Google Ads API: For extracting ad performance data from Google.
   - AWS Lambda: For running extraction jobs, particularly for incremental data fetching.
   - AWS S3: For staging raw extracted data before transformation.

2. **Data Transformation**:
   - AWS Glue: For data transformation, cleaning, and normalization.
   - Apache Spark (within AWS Glue): For scalable data processing.
   - AWS Step Functions: For orchestrating the transformation workflows.

3. **Data Loading**:
   - AWS RDS: For storing the transformed data in a relational database.
   - AWS Data Pipeline (Optional): For managing data movement and workflow dependencies.

4. **Orchestration and Scheduling**:
   - Apache Airflow: For scheduling and managing the entire ETL process through Directed Acyclic Graphs (DAGs).

5. **Monitoring and Error Handling**:
   - AWS CloudWatch: For monitoring ETL jobs and setting up alerts for failures and performance issues.
   - AWS SNS: For sending notifications and alerts based on CloudWatch metrics.

6. **Security**:
   - AWS KMS: For encrypting data at rest and in transit.
   - AWS IAM: For managing access controls and permissions.

### ETL Tool: Apache Airflow

Apache Airflow will be used as the primary ETL orchestration tool. It will schedule and manage the ETL workflows, handle dependencies, and ensure that the entire pipeline runs smoothly.

### ETL Pipeline Flow

1. **Data Extraction**:
   - **Step 1**: Airflow triggers AWS Lambda functions to extract data from Facebook Ads API and Google Ads API.
   - **Step 2**: Extracted data is stored in raw format in an S3 bucket.

2. **Data Transformation**:
   - **Step 3**: Airflow triggers AWS Glue jobs to process the raw data.
     - **Sub-Step 3.1**: Glue jobs clean, normalize, and aggregate the data.
     - **Sub-Step 3.2**: Transformations handle schema evolution and data quality checks.
   - **Step 4**: Transformed data is temporarily stored in another S3 bucket.

3. **Data Loading**:
   - **Step 5**: Airflow triggers a data loading job (could be a Lambda function or a Glue job based on the volume being handled) to load the transformed data from S3 into an RDS database.
   - **Step 6**: Bulk loading operations are used to optimize database insertions.

4. **Monitoring and Error Handling**:
   - **Step 7**: AWS CloudWatch monitors the extraction, transformation, and loading processes.
     - **Sub-Step 7.1**: Logs and metrics are collected for each step.
     - **Sub-Step 7.2**: Errors are captured, and retry mechanisms are implemented.
   - **Step 8**: AWS SNS sends alerts and notifications in case of failures or performance issues.

5. **Scalability**:
   - **Step 9**: AWS Lambda and Glue jobs scale automatically based on the data volume and processing requirements.
   - **Step 10**: Apache Airflow dynamically adjusts the workflow execution based on task dependencies and resource availability.
  
   ![ETL Pipeline Diagram](diagrams/ETL_Pipeline_Diagram.png)
