import pandas as pd
import boto3
import requests
from datetime import date
from botocore.client import Config
import json
import time
import io
from airflow.operators.python_operator import PythonOperator
from airflow import DAG
from airflow.models import Variable
from airflow.utils.trigger_rule import TriggerRule
from airflow import configuration
from datetime import datetime, timedelta
from pendulum import timezone
from airflow.contrib.hooks.snowflake_hook import SnowflakeHook
from airflow.contrib.operators.snowflake_operator import SnowflakeOperator

AWS_ACCESS_KEY = Variable.get('AWS_SECRET_KEY')
AWS_SECRET_ACCESS_KEY = Variable.get('AWS_SECRET_ACCESS_KEY')
API_SECRET = Variable.get('SECRET_TOKEN_API')

default_args = {
    'owner': 'dmitry_prosimplee',
    'email': 'prosimplee@gmail.com',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


def extract_fact_flights(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, API_SECRET):
    url = "https://flight-radar1.p.rapidapi.com/flights/list-most-tracked"
    headers = {
        "X-RapidAPI-Key": API_SECRET,
        "X-RapidAPI-Host": "flight-radar1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    bucket_name = "planes-snowflake-prosimplee"
    file_name = str(date.today()) + "/bronze_data/flights_raw.json"
    s3 = boto3.resource('s3',
                        aws_access_key_id=AWS_ACCESS_KEY,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        config=Config(signature_version='s3v4')
                        )
    try:
        s3.Bucket(bucket_name).put_object(Key=file_name, Body=json.dumps(data['data']), ACL='private')
        print('Data was successfully put into bronze S3 bucket!')
    except ValueError:
        print('Put data to bronze S3 bucket: FAILURE!')


def extract_airports(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, API_SECRET):
    url = "https://flight-radar1.p.rapidapi.com/aircrafts/list"
    headers = {
        "X-RapidAPI-Key": API_SECRET,
        "X-RapidAPI-Host": "flight-radar1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    bucket_name = "planes-snowflake-prosimplee"
    file_name = str(date.today()) + "/bronze_data/planes_raw.json"
    s3 = boto3.resource('s3',
                        aws_access_key_id=AWS_ACCESS_KEY,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        config=Config(signature_version='s3v4')
                        )
    try:
        s3.Bucket(bucket_name).put_object(Key=file_name, Body=json.dumps(data['rows']), ACL='private')
        print('Data was successfully put into bronze S3 bucket!')
    except ValueError:
        print('Put data to bronze S3 bucket: FAILURE!')


create_temp_table_planes = ["""
                            create or replace table RAW.RAW_PLANES_DATA
                               (json_data  variant 
                            );"""]

create_temp_table_flights = ["""
                            create or replace table RAW.RAW_FLIGHTS_DATA 
                                (json_data  variant 
                                );"""]


def s3_to_snowflake_planes_raw(date_today):
    SnowflakeHook(
        snowflake_conn_id='snowflake_con'
    ).run(f"""copy into FLIGHTS_PET.RAW.RAW_PLANES_DATA
             from @BRONZE_STAGE
             files = ('{date_today}/bronze_data/planes_raw.json')
             file_format = ( format_name='JSON_FORMAT')
    """)


def s3_to_snowflake_flights_raw(date_today):
    SnowflakeHook(
        snowflake_conn_id='snowflake_con'
    ).run(f"""copy into FLIGHTS_PET.RAW.RAW_FLIGHTS_DATA
             from @BRONZE_STAGE
             files = ('{date_today}/bronze_data/flights_raw.json')
             file_format = ( format_name='JSON_FORMAT')
    """)


def raw_planes_to_dw_planes():
    SnowflakeHook(
        snowflake_conn_id='snowflake_con'
    ).run(f""" INSERT INTO PUBLIC.PLANES (id, plane_name, plane_code)
              select seq_1_1.nextval,
                     f.value:Name::string ,
                     f.value:Code::string 
              from FLIGHTS_PET.RAW.RAW_PLANES_DATA, table(flatten($1:models)) as f """)


def raw_flights_to_dw_flights():
    SnowflakeHook(
        snowflake_conn_id='snowflake_con'
    ).run(""" INSERT INTO PUBLIC.FLIGHTS(flight_id, from_city, to_city, plane_model)
              select json_data:flight_id::varchar, 
                     json_data:from_city::varchar, 
                     json_data:to_city::varchar, 
                     json_data:model
              from FLIGHTS_PET.RAW.RAW_FLIGHTS_DATA""")


date_today = date.today()

with DAG(
        dag_id='planes_snowflake_s3',
        start_date=datetime(2022, 9, 12),  # makes sense if Catchup = True
        schedule_interval='50 13 * * *',
        catchup=False,
        default_args=default_args
) as dag:
    PythonOperator(
        task_id='extract_fact_flights',
        python_callable=extract_fact_flights,
        op_kwargs={'AWS_ACCESS_KEY': AWS_ACCESS_KEY,
                   'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY,
                   'API_SECRET': API_SECRET}
    )

    PythonOperator(
        task_id='extract_airports',
        python_callable=extract_airports,
        op_kwargs={'AWS_ACCESS_KEY': AWS_ACCESS_KEY,
                   'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY,
                   'API_SECRET': API_SECRET}
    )

    SnowflakeOperator(
        task_id='create_temp_table_planes',
        snowflake_conn_id="snowflake_con",
        sql=create_temp_table_planes
    )

    SnowflakeOperator(
        task_id='create_temp_table_flights',
        snowflake_conn_id="snowflake_con",
        sql=create_temp_table_flights
    )

    PythonOperator(
        task_id='s3_to_snowflake_planes_raw',
        python_callable=s3_to_snowflake_planes_raw,
        op_kwargs={'date_today': str(date_today)}
    )
    PythonOperator(
        task_id='s3_to_snowflake_flights_raw',
        python_callable=s3_to_snowflake_flights_raw,
        op_kwargs={'date_today': str(date_today)}
    )

    PythonOperator(
        task_id='raw_planes_to_dw_planes',
        python_callable=raw_planes_to_dw_planes
    )

    PythonOperator(
        task_id='raw_flights_to_dw_flights',
        python_callable=raw_flights_to_dw_flights
    )

    t = dag.task_dict

    t['extract_fact_flights'] >> t['extract_airports'] \
    >> [t['create_temp_table_planes'], t['create_temp_table_flights']] \
    >> t['s3_to_snowflake_planes_raw'] >> t['s3_to_snowflake_flights_raw'] \
    >> t['raw_planes_to_dw_planes'] >> t['raw_flights_to_dw_flights']
