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
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

tables_dir = Variable.get('TABLES_DIR')

def select_tables_covid_db(dt, schema_name):
    with open (f'{tables_dir}/covid_db_tables/{dt}_{schema_name}_tables_name.csv', 'w') as file:
        sql="""
                SELECT schemaname , tablename , tableowner 
                FROM pg_catalog.pg_tables
                WHERE schemaname != 'pg_catalog' AND 
                      schemaname != 'information_schema'
                """
        pg_hook = PostgresHook(postgres_conn_id='postgres_tables', schema=schema_name)
        pg_conn = pg_hook.get_conn()
        cursor = pg_conn.cursor()
        cursor.execute(sql)
        df = pd.DataFrame(cursor.fetchall())
        df.columns = ['schema_name', 'table_name', 'table_owner']
        df.to_csv(file, header = True, index = False, sep = '|')


def select_tables_postgresql(dt, schema_name):
    with open (f'{tables_dir}/postgresql_db_tables/{dt}_{schema_name}_tables_name.csv', 'w') as file:
        sql="""
                SELECT schemaname , tablename , tableowner 
                FROM pg_catalog.pg_tables
                WHERE schemaname != 'pg_catalog' AND 
                      schemaname != 'information_schema'
                """
        pg_hook = PostgresHook(postgres_conn_id='postgres_tables', schema=schema_name)
        pg_conn = pg_hook.get_conn()
        cursor = pg_conn.cursor()
        cursor.execute(sql)
        df = pd.DataFrame(cursor.fetchall())
        df.columns = ['schema_name', 'table_name', 'table_owner']
        df.to_csv(file, header = True, index = False, sep = '|')


default_args = {
    'owner': 'dmitry',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'email_on_failure': True
}


with DAG(
        dag_id='db_tables',
        start_date=datetime(2022, 3, 9, tzinfo=timezone('Europe/Moscow')),
        schedule_interval='0 10 20 * *',
        catchup=False,
        default_args=default_args
) as dag:
    today = "{{ next_execution_date.in_timezone('Europe/Moscow').strftime('%Y-%m-%d') }}"

    PythonOperator(
        task_id='select_tables_covid_db',
        python_callable=select_tables_covid_db,
        op_kwargs = {'dt': today,
                     'schema_name' : 'covid_db'}
    )

    PythonOperator(
        task_id='select_tables_postgresql',
        python_callable=select_tables_postgresql,
        op_kwargs={'dt': today,
                   'schema_name': 'postgresql'}
    )

    t = dag.task_dict
    t['select_tables_covid_db']
    t['select_tables_postgresql']

