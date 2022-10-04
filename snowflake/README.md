# Snowflake + S3 + API + Airflow + Python. The Snoflake Pipe below is available using SQS + S3.
 
Some steps to download data from AWS S3 Bucket to Snowflake

1. We create a storage system integrator
```sql
CREATE OR REPLACE STORAGE INTEGRATION s3_integration_full
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER = s3
STORAGE_AWS_ROLE_ARN = 'ROLE ARN'
ENABLED = true
STORAGE_ALLOWED_LOCATIONS = ('S3 Bucket URL');
```

2. Here it is important to write out the value of the fields: STORAGE_AWS_IAM_USER_ARN & STORAGE_AWS_EXTERNAL_ID
```sql
DESCRIBE STORAGE INTEGRATION s3_integration_full; 
```

3. Put these values in Roles -> Your Role -> Trust relationships -> Trusted Entites -> Edit trust policy

![image](https://user-images.githubusercontent.com/55916170/189838088-af57baef-9da2-437d-b813-6676917c750d.png)

4. Create a stage (Paragraph 1)
```sql
CREATE OR REPLACE STAGE RAW.bronze_stage
URL = 'S3 Bucket URL'
STORAGE_INTEGRATION = s3_integration_full;
```


5. Create File Format for JSON
```sql
CREATE FILE FORMAT "FLIGHTS_PET"."PUBLIC".JSON_FORMAT 
TYPE = 'JSON' 
COMPRESSION = 'AUTO' 
ENABLE_OCTAL = FALSE 
ALLOW_DUPLICATE = FALSE 
STRIP_OUTER_ARRAY = TRUE 
STRIP_NULL_VALUES = FALSE 
IGNORE_UTF8_ERRORS = FALSE;
```

6. Create a TEMPORARY TABLE
```sql
CREATE OR REPLACE TEMPORARY TABLE RAW.raw_planes_data (
json_data  variant 
);
```

7. Copy data from S3 Bucket to TEMPORARY TABLE
```sql
COPY INTO FLIGHTS_PET.RAW.RAW_PLANES_DATA
FROM @BRONZE_STAGE -- our S3 Bucket
FILES = ('{date_today}/bronze_data/planes_raw.json') -- folder_name/stage_name/file_name
FILE_FORMAT = ( format_name='JSON_FORMAT') -- our file_format (Paragraph 5)
```

8. Create PUBLIC.TABLE
```sql
CREATE OR REPLACE TABLE PUBLIC.PLANES
(id number, 
plane_name varchar (30),
plane_code varchar (30))
```

8. Load files from RAW.TEMP_TABLE to PUBLIC.TABLE
```sql
INSERT INTO PUBLIC.PLANES(id, plane_name, plane_code)
SELECT seq_1_1.nextval,
       f.value:Name::string as name,
       f.value:Code::string as plane_code
FROM RAW.RAW_PLANES_DATA, TABLE(flatten($1:models)) f;
```

9. All is ready !!!
```sql
SELECT *
FROM PUBLIC.PLANES
```
![image](https://user-images.githubusercontent.com/55916170/189858903-c3f11708-6365-4d53-bd82-0977984b2ffb.png)

[Planes Pipeline is available by the link ](https://github.com/prosimpleee/data_engineering_/blob/main/snowflake/dags/planes_snowflake_s3.py)


# Snowflake Pipe + SQS + S3

1. Create DB & Schema
```sql
CREATE DATABASE snow_pipe_superstore ;

CREATE SCHEMA raw_snow_pipe ;
```

2. Create storage integration (S3 & Snowflake)
```sql
CREATE OR REPLACE STORAGE INTEGRATION s3_int
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER = s3
STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::256535007744:role/snow-pipe-superstore-role' -- Our Role
ENABLED = true
STORAGE_ALLOWED_LOCATIONS = ('s3://snow-pipe-superstore/') ; -- Our S3 Bucket
```

3. Important values for change "Trust relationships" in our Role
```sql
DESC INTEGRATION s3_int ;
```
![image](https://user-images.githubusercontent.com/55916170/190140266-73c7596f-8fd8-4f13-ac37-7d65f066c4a7.png)

4. Put the values (STORAGE_AWS_IAM_USER_ARN & STORAGE_AWS_EXTERNAL_ID) into AWS Role 
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "STORAGE_AWS_IAM_USER_ARN"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "STORAGE_AWS_EXTERNAL_ID"
                }
            }
        }
    ]
}
```

5. Сreate a place where we will take the data
```sql
CREATE OR REPLACE STAGE raw_snow_pipe.raw_superstore_data
URL = 's3://snow-pipe-superstore'
STORAGE_INTEGRATION = s3_int ; -- Our Storage Integration (Paragraph 2)
```

6. Create File Format for CSV using sql script
```sql
 CREATE or replace FILE FORMAT RAW_SNOW_PIPE.CSV_FORMAT 
 TYPE = 'CSV' 
 COMPRESSION = 'AUTO' 
 FIELD_DELIMITER = ',' 
 RECORD_DELIMITER = '\n' 
 SKIP_HEADER = 1 
 FIELD_OPTIONALLY_ENCLOSED_BY = 'NONE' 
 TRIM_SPACE = FALSE 
 ERROR_ON_COLUMN_COUNT_MISMATCH = TRUE 
 ESCAPE = 'NONE' 
 ESCAPE_UNENCLOSED_FIELD = '\134' 
 DATE_FORMAT = 'AUTO' 
 TIMESTAMP_FORMAT = 'AUTO' 
 NULL_IF = ('\\N') ;
 ```
 
 7. Create a table where data will be added
 ```sql
  CREATE OR REPLACE TABLE RAW_SNOW_PIPE.STAGE_RAW_SUPERSTORE( 
 Row_number int,
 Raw_ID text,
 Order_ID text,
 Order_Date date,
 Ship_Date text,
 Ship_Mode text, 
 Customer_ID text, 
 Customer_Name text,
 Segment text,
 Country text,
 City text,
 State text,	
 Postal_Code int,
 Region text,
 Product_ID text,
 Category text,
 Sub_Category text,
 Product_Name text,
 Sales text,
 Quantity int,
 Discount float,
 Profit float ;)
 ```

8. Creating our Snowflake Pipe
```sql
CREATE OR REPLACE PIPE RAW_SNOW_PIPE.superstore_pipe
AUTO_INGEST = true as 
COPY INTO RAW_SNOW_PIPE.STAGE_RAW_SUPERSTORE -- Our table (Paragraph 7)
FROM @raw_snow_pipe.raw_superstore_data -- Our Stage (Paragraph 5)
FILE_FORMAT = CSV_FORMAT
ON_ERROR="CONTINUE" ;
```

9. Here we need a field: notification_channel
```sql
SHOW PIPES ;
```

10. We put the value (notification_channel) to YourBucket -> Properties -> Event notifications -> Destination -> SQS queue -> Enter SQS queue ARN

![image](https://user-images.githubusercontent.com/55916170/190142961-bf00cfb8-6b8a-4be9-b1c0-a42165683339.png)

11. Displaying the status of our pipe. Should be : RUNNING
```sql
SELECT system$pipe_status('RAW_SNOW_PIPE.superstore_pipe') ;
```

12. Upload your CSV file to S3 Bucket and wait few second !!!

13. We can see how correctly our data loaded into the our table in Snowflake (RAW_SNOW_PIPE.STAGE_RAW_SUPERSTORE)
```sql
SELECT *
FROM table (INFORMATION_SCHEMA.copy_history(table_name=> 'RAW_SNOW_PIPE.STAGE_RAW_SUPERSTORE', start_time=> dateadd(hours, -1, current_timestamp())))
```

14. Making a SELECT and looking at our data :)
```sql
SELECT * 
FROM RAW_SNOW_PIPE.STAGE_RAW_SUPERSTORE
```

![image](https://user-images.githubusercontent.com/55916170/190147209-ad853762-a175-4705-a28f-98c31a7eb08e.png)



