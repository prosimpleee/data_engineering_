# Snowflake + S3 + Airflow + Python

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




