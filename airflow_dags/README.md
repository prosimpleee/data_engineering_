# Airflow

I used Airflow to orchestrate ETL processes. It was possible to set up airflow based on PostgreSQL for meta data.

## Import Lib:
```python
import requests
import json
import pandas as pd
import datetime
import sqlalchemy as sa
import sys
from airflow.operators.python_operator import PythonOperator
from airflow import DAG
from datetime import datetime, timedelta
from pendulum import timezone
import requests
from airflow.models import Variable
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import numpy as np
```

## Defaul args:
```python
default_args = {
      'owner': 'owner_name',
      'retries': 1,                       #cnt of retries after fail
      'retry_delay': timedelta(minutes=5) # repetition rate
}
```

## Create a DAG:
```python
with DAG(
       dag_id='dag_name',
       start_date=datetime(2022, 3, 7, tzinfo=timezone('Europe/Moscow')), # dag start date
       schedule_interval='10 13 * * *',                                   # cron syntax in the job scheduler
       catchup=True,
       default_args=default_args
) as dag:
```
## Dags:
- [Covid Status ETL](https://github.com/prosimpleee/data_engineering_/blob/main/airflow_dags/covid_status_etl/covid_status.py) 
- [Currency ETL](https://github.com/prosimpleee/data_engineering_/blob/main/airflow_dags/currency_etl/currency_etl.py) 
- [Tables Names](https://github.com/prosimpleee/data_engineering_/blob/main/airflow_dags/tables_prod_postgresql/tables_prod.py) 
- [Traders Data](https://github.com/prosimpleee/data_engineering_/blob/main/airflow_dags/traders_data/extract_traders_data.py) 
