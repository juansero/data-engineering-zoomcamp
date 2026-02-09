# Module 3 Homework: Data Warehousing

This repository contains the solution for the Module 3 homework of the Data Engineering Zoomcamp 2026.

## 🛠️ Setup

### 1. Data Loading
The data for **Yellow Taxi Trip Records (Jan 2024 - Jun 2024)** was loaded into a Google Cloud Storage (GCS) bucket using the python script `load_data.py`.

### 2. BigQuery Setup
I created an external table and a materialized (non-partitioned) table to start the analysis:

```sql
-- Create External Table
CREATE OR REPLACE EXTERNAL TABLE `ny_taxi_2024.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://YOUR_BUCKET_NAME/yellow_tripdata_2024-*.parquet']
);

-- Create Materialized Table
CREATE OR REPLACE TABLE `ny_taxi_2024.yellow_tripdata_non_partitioned` AS
SELECT * FROM `ny_taxi_2024.external_yellow_tripdata`;

Homework Questions
Question 1: Counting records
Answer: 20,332,093

Query:

SQL
SELECT count(*) FROM `ny_taxi_2024.yellow_tripdata_non_partitioned`;
Question 2: Data read estimation
Answer: 0 MB for the External Table and 155.12 MB for the Materialized Table

Queries used for estimation:

SQL
-- External Table (Estimates 0 MB or inaccurate)
SELECT DISTINCT(PULocationID) FROM `ny_taxi_2024.external_yellow_tripdata`;

-- Materialized Table (Estimates 155.12 MB)
SELECT DISTINCT(PULocationID) FROM `ny_taxi_2024.yellow_tripdata_non_partitioned`;
Question 3: Understanding columnar storage
Answer: BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

Question 4: Zero fare trips
Answer: 8,333

Query:

SQL
SELECT count(*) 
FROM `ny_taxi_2024.yellow_tripdata_non_partitioned`
WHERE fare_amount = 0;
Question 5: Partitioning and clustering strategy
Answer: Partition by tpep_dropoff_datetime and Cluster on VendorID

Question 6: Partition benefits
Answer: 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table

Step 1: Create the optimized table

SQL
CREATE OR REPLACE TABLE `ny_taxi_2024.yellow_tripdata_partitioned`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `ny_taxi_2024.external_yellow_tripdata`;
Step 2: Compare queries

SQL
-- Scans ~310.24 MB
SELECT DISTINCT(VendorID)
FROM `ny_taxi_2024.yellow_tripdata_non_partitioned`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

-- Scans ~26.84 MB
SELECT DISTINCT(VendorID)
FROM `ny_taxi_2024.yellow_tripdata_partitioned`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';
Question 7: External table storage
Answer: GCP Bucket

Question 8: Clustering best practices
Answer: False

Question 9: Count(*) estimates
Answer: 0 Bytes

Reasoning: BigQuery stores metadata about tables, including the row count. When performing a COUNT(*) without any filters, BigQuery retrieves this value directly from the metadata rather than scanning the actual table rows.