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
from airflow.providers.telegram.operators.telegram import TelegramOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.providers.telegram.hooks.telegram import TelegramHook
from airflow import configuration
from datetime import datetime, timedelta
from pendulum import timezone

AWS_ACCESS_KEY = Variable.get('AWS_SECRET_KEY')
AWS_SECRET_ACCESS_KEY = Variable.get('AWS_SECRET_ACCESS_KEY')
API_SECRET = Variable.get('SECRET_TOKEN_API')
SECRET_CHAT_ID = Variable.get('SECRET_CHAT_ID')


def task_success_alert(context):
    dag_id = context['dag'].dag_id
    task_id = context['task_instance'].task_id
    TelegramHook(telegram_conn_id='airflow_not_trad_bot').send_message(
        {'text': 'Name DAG: ' + dag_id + '\n' + 'Task Name: ' + task_id + ' completed successfully!'})


def task_failure_alert(context):
    dag_id = context['dag'].dag_id
    task_id = context['task_instance'].task_id
    execution_date = context['ts']
    url = context['task_instance'].log_url
    # exception = context['exception']

    failed_alert = TelegramOperator(
        task_id='tg_failed',
        telegram_conn_id='telegram_con_failed',
        text='Failure on: ' + dag_id + '\n' + 'Task Name: ' + task_id + ' FAILED!!!' + 'Task: ' + execution_date +
             '\n' + 'Logs: ' + url + '|to Airflow UI')
    return failed_alert.execute(context=context)


default_args = {
    'owner': 'dmitry_prosimplee',
    'email': 'prosimplee@gmail.com',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'on_success_callback': task_success_alert,
    'on_failure_callback': task_failure_alert
}


def extract_traders_data_tos3(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, API_SECRET):
    url = "https://rest.coinapi.io/v1/trades/latest"
    headers = {'X-CoinAPI-Key': API_SECRET}
    response = requests.get(url, headers=headers)
    data = response.json()
    bucket_name = "traders-api-data"
    file_name = str(date.today()) + "/bronze_data/bronze_traders_data.json"
    s3 = boto3.resource('s3',
                        aws_access_key_id=AWS_ACCESS_KEY,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        config=Config(signature_version='s3v4')
                        )
    try:
        s3.Bucket(bucket_name).put_object(Key=file_name, Body=json.dumps(data), ACL='private')
        print('Data was successfully put into bronze S3 bucket!')
    except ValueError:
        print('Put data to bronze S3 bucket: FAILURE!')


def extract_dictionary_currency_data(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, API_SECRET):
    url = "https://rest.coinapi.io/v1/assets"
    headers = {"X-CoinAPI-Key": API_SECRET}
    response = requests.get(url, headers=headers)
    crypto_dictionary = []
    for cr_n in response.json():
        try:
            dictionary_crypto = {"symbol_id": cr_n["asset_id"],
                                 "symbol_name": cr_n["name"]}
            crypto_dictionary.append(dictionary_crypto)
        except ValueError:
            print("Crypto Name ValueError!")
    df = pd.DataFrame(crypto_dictionary)
    bucket_name = "traders-api-data"
    file_name = "dictionary_data/dictionary.csv"
    s3 = boto3.resource("s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    try:
        s3.Bucket(bucket_name).put_object(Key=file_name, Body=df.to_csv(index=False), ACL="private")
        print("Dictionary was successfully put into S3 bucket!")
    except ValueError:
        print("Extract Crypto Dictionary via Api: FAILED!")


def transform_bronze_traders_data(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY):
    s3_traders = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    content_object_traders = s3_traders.Object('traders-api-data',
                                               str(date.today()) + "/bronze_data/bronze_traders_data.json")
    file_content_traders = content_object_traders.get()['Body'].read().decode('utf-8')
    data_traders_bronze = json.loads(file_content_traders)
    df_silver_list = []
    for data in data_traders_bronze:
        if 'uuid' in data.keys():
            df_silver_list.append({'user_id': data['uuid'],
                                   'symbol_from_to': data['symbol_id'],
                                   'time_exchange': data['time_exchange'],
                                   'size': data['size'],
                                   'action': data['taker_side']})

    tr_df = pd.DataFrame(df_silver_list)
    bucket_name = "traders-api-data"
    file_name = str(date.today()) + "/silver_data/silver_traders_data.csv"
    s3 = boto3.resource("s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    try:
        s3.Bucket(bucket_name).put_object(Key=file_name, Body=tr_df.to_csv(index=False), ACL="private")
        print("Data was successfully put into silver S3 bucket!")
    except ValueError:
        print("Put data to silver S3 bucket: FAILURE!")
    time.sleep(3)


def transform_silver_traders_data(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY):
    # Traders part
    s3_traders = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    content_object_traders = s3_traders.get_object(Bucket='traders-api-data',
                                                   Key=str(date.today()) + "/silver_data/silver_traders_data.csv")
    df_traders = pd.read_csv(io.BytesIO(content_object_traders['Body'].read()))
    df_traders['symbol_from'] = df_traders['symbol_from_to'].str.split('_', expand=True)[2]
    df_traders['symbol_to'] = df_traders['symbol_from_to'].str.split('_', expand=True)[3]

    updated_df_traders = df_traders[['user_id', 'time_exchange', 'size', 'action', 'symbol_from', 'symbol_to']]

    # Dictionary part
    s3_dictionary = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    content_object_dictionary = s3_dictionary.get_object(Bucket='traders-api-data',
                                                         Key="dictionary_data/dictionary.csv")

    df_dictionary = pd.read_csv(io.BytesIO(content_object_dictionary['Body'].read()))

    try:
        join_dfs_from = pd.merge(updated_df_traders, df_dictionary, left_on='symbol_from', right_on='symbol_id')
        updated_df_traders = join_dfs_from[['user_id', 'time_exchange', 'size', 'action', 'symbol_name', 'symbol_to']]
        updated_df_traders = updated_df_traders.rename(columns={'symbol_name': 'symbol_from_txt'})
        join_dfs_to = pd.merge(updated_df_traders, df_dictionary, left_on='symbol_to', right_on='symbol_id')
        all_traders_data = join_dfs_to.rename(columns={'symbol_name': 'symbol_to_txt'})
        all_traders_data = all_traders_data[['user_id',
                                             'time_exchange',
                                             'size',
                                             'symbol_from_txt',
                                             'symbol_to_txt',
                                             'action']]

        try:
            bucket_name = "traders-api-data"
            file_name = str(date.today()) + "/golden_data/golden_traders_data.csv"
            s3 = boto3.resource("s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            s3.Bucket(bucket_name).put_object(Key=file_name, Body=all_traders_data.to_csv(index=False), ACL="private")
            print(all_traders_data)
            print("Data was successfully put into golden S3 bucket!")
        except ValueError:
            print("Put data to golden S3 bucket: FAILURE!")
    except ValueError:
        print('Merge 2 df with mistake !')


with DAG(
        dag_id='extract_traders_data',
        start_date=datetime(2022, 8, 29, tzinfo=timezone('Europe/Moscow')),  # makes sense if Catchup = True
        schedule_interval='10 17 * * *',
        catchup=False,
        default_args=default_args
) as dag:
    today = "{{ next_execution_date.in_timezone('Europe/Moscow').strftime('%Y-%m-%d') }}"

    PythonOperator(
        task_id='extract_traders_data_tos3',
        python_callable=extract_traders_data_tos3,
        op_kwargs={'AWS_ACCESS_KEY': AWS_ACCESS_KEY,
                   'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY,
                   'API_SECRET': API_SECRET}
    )

    PythonOperator(
        task_id='extract_dictionary_currency_data',
        python_callable=extract_dictionary_currency_data,
        op_kwargs={'AWS_ACCESS_KEY': AWS_ACCESS_KEY,
                   'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY,
                   'API_SECRET': API_SECRET}
    )

    PythonOperator(
        task_id='transform_bronze_traders_data',
        python_callable=transform_bronze_traders_data,
        op_kwargs={'AWS_ACCESS_KEY': AWS_ACCESS_KEY,
                   'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY}
    )

    PythonOperator(
        task_id='transform_silver_traders_data',
        python_callable=transform_silver_traders_data,
        op_kwargs={'AWS_ACCESS_KEY': AWS_ACCESS_KEY,
                   'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY}
    )

    t = dag.task_dict

    [t['extract_traders_data_tos3'], t['extract_dictionary_currency_data']] >> t['transform_bronze_traders_data'] \
    >> t['transform_silver_traders_data']
