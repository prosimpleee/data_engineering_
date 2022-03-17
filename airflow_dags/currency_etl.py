import requests
import json
import pandas as pd
from datetime import datetime as change_data
import datetime
import sqlalchemy as sa
import sys
from airflow.operators.python_operator import PythonOperator
from airflow import DAG
from datetime import datetime, timedelta
from pendulum import timezone
import requests
from airflow.models import Variable
from datetime import date
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.providers.telegram.operators.telegram import TelegramOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.providers.telegram.hooks.telegram import TelegramHook
from airflow import configuration


token = Variable.get('SECRET_COIN_MARKET')
chat_id_tg = Variable.get('chat_id_tg')
data_dir = Variable.get('DATA_DIR')



# Extract data from API
def extract_data(dt):
    with open(f'{data_dir}/bronze/currency_etl/{dt}_v6_currency.json', 'w') as f:
        url = f'https://v6.exchangerate-api.com/v6/{token}/latest/USD'
        response = requests.get(url)
        data = response.json()
        json.dump(data, f)


# Transform data
def transform_data(dt):
    with open(f'{data_dir}/bronze/currency_etl/{dt}_v6_currency.json', 'r') as json_file:
        all_currency = json.load(json_file)
        list_currency = [{'CurrencyName': base,
                          'Value': value} for base, value in all_currency['conversion_rates'].items() if
                         base in ('EUR', 'USD', 'GBP')]
        df = pd.DataFrame(list_currency)
        df['CreatedTimestamp'] = change_data.strptime(all_currency['time_last_update_utc'], '%a, %d %b %Y %H:%M:%S +%f')
        df.to_parquet(f'{data_dir}/silver/currency_etl/{dt}_v6_currency.parquet')


# Load into db
def insert_mssql_hook(dt):
    # mssql_hook = MsSqlHook(mssql_conn_id='airflow_mssql', schema='airflow')
    df = pd.read_parquet(f'{data_dir}/silver/currency_etl/{dt}_v6_currency.parquet')
    target_fields = list(df.columns)
    # print(target_fields)

    rows = [list(row)[1::] for row in df.itertuples()]
    mssql_hook = MsSqlHook(mssql_conn_id='airflow_mssql')
    # print(rows[1])

    # mssql_hook.run(sql = 'DELETE FROM [dbo].[dim.Currency]')
    # Insert tows
    mssql_hook.insert_rows(table='[dbo].[dim.Currency]', rows=rows, target_fields=target_fields)


# Callback
def task_success_alert(context):
    dag_id = context['dag'].dag_id
    task_id = context['task_instance'].task_id
    TelegramHook(telegram_conn_id='teleram_con_success').send_message(
        {'text': 'Name DAG: ' + dag_id + '\n' + 'Task Name: ' + task_id + 'completed successfully!'})


def task_failure_alert(context):
    dag_id = context['dag'].dag_id
    task_id = context['task_instance'].task_id
    execution_date = context['ts']
    url = context['task_instance'].log_url
    # exception = context['exception']

    failed_alert = TelegramOperator(
        task_id = 'tg_failed',
        telegram_conn_id='telegram_con_failed',
        text = 'Failure on: ' + dag_id + '\n' + 'Task Name: ' + task_id + ' FAILED!!!' + 'Task: ' + execution_date +
               '\n' + 'Logs: ' + url + '|to Airflow UI')
    return failed_alert.execute(context=context)



default_args = {
    'owner': 'dmitry',
    'email': 'prosimplee@gmail.com',
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'on_success_callback': task_success_alert,
    'on_failure_callback': task_failure_alert
    # 'email_on_failure': True
}

with DAG(
        dag_id='currency_etl',
        start_date=datetime(2022, 3, 8, tzinfo=timezone('Europe/Moscow')),
        schedule_interval='47 10 * * *',
        catchup=True,
        default_args=default_args
) as dag:

    today = "{{ next_execution_date.in_timezone('Europe/Moscow').strftime('%Y-%m-%d') }}"

    # Extract data
    PythonOperator(
        task_id='extract_op',
        python_callable=extract_data,
        op_kwargs={'dt': today}
    )

    # Transform data
    PythonOperator(
        task_id='transform_op',
        python_callable=transform_data,
        op_kwargs={'dt': today}
    )

    # Load data into db
    PythonOperator(
        task_id='load_op',
        python_callable=insert_mssql_hook,
        op_kwargs={'dt': today}
    )


    t = dag.task_dict

    t = dag.task_dict
    t['extract_op'] >> t['transform_op'] >> t['load_op']
