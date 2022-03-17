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
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import numpy as np

covid_token = Variable.get('COVID_TOKEN')
data_dir = Variable.get('DATA_DIR')


def extract_covid_statistics(dt):
    with open(f'{data_dir}/bronze/covid_stat/{dt}_covid_statistics.json', 'w') as file:
        url = "https://covid-193.p.rapidapi.com/statistics"

        headers = {
            'x-rapidapi-host': "covid-193.p.rapidapi.com",
            'x-rapidapi-key': f"{covid_token}"
        }

        response = requests.get(url, headers=headers)

        data = response.json()
        json.dump(data, file)
        print('--------------------------------Success Extract from API------------------------------------')


def transform_covid_data(dt):
    with open(f'{data_dir}/bronze/covid_stat/{dt}_covid_statistics.json', 'r') as ff:
        data = json.load(ff)

        covid_statistics = [{'continent': i['continent'], 'country': i['country'], 'population': i['population'],
                             'confirmed': i['cases']['new'], 'active': i['cases']['active'],
                             'recovered': i['cases']['recovered'], 'deaths': i['deaths']['new'],
                             'created_timestamp': i['time']} for i in data['response']]

        df = pd.DataFrame(covid_statistics)
        df[['confirmed', 'active', 'recovered', 'deaths']] = \
            df[['confirmed', 'active', 'recovered', 'deaths']].fillna(value=0)

        df = df.astype({'confirmed': 'int', 'active': 'int', 'recovered': 'int', 'deaths': 'int'})

        new_df = df.query('country!=continent')

        new_df.to_parquet(f'{data_dir}/silver/covid_stat/{dt}_covid_statistics.parquet')
        print('-----------------------------------Success Saved to Parquet---------------------------------')


def calculations_to_analyst(dt):
    spark = SparkSession.builder.master('local[2]').getOrCreate()
    spark \
        .read \
        .option('header', True) \
        .parquet(f'{data_dir}/silver/covid_stat/{dt}_covid_statistics.parquet') \
        .createOrReplaceTempView('covid_stat')

    df = spark.table('covid_stat')
    sum_statistics = df.groupBy('continent',
                                F.date_trunc('hour', 'created_timestamp').alias('created_timestamp')) \
        .agg(
            F.sum('confirmed').alias('confirmed_cnt_by_cont'),
            F.sum('active').alias('active_cnt_by_cont'),
            F.sum('recovered').alias('recovered_cnt_by_cont'),
            F.sum('deaths').alias('deaths_cnt_by_cont')) \
        .where('continent not in ("None", "All")')\
        .select('continent', 'confirmed_cnt_by_cont', 'active_cnt_by_cont',
                'recovered_cnt_by_cont', 'deaths_cnt_by_cont', 'created_timestamp')
    sum_statistics.write.parquet(f'{data_dir}/gold/covid_stat/{dt}_covid_statistics.parquet')
    print('-----------------------------------Success AGG---------------------------------')


def loading_postgres_fact(dt):
    df = pd.read_parquet(f'{data_dir}/silver/covid_stat/{dt}_covid_statistics.parquet')
    pg_hook = PostgresHook(postgres_conn_id='postgres_localhost')
    rows = [list(row) for row in df.itertuples()]
    target_field = list(df.columns)
    pg_hook.insert_rows(table='covid_statistics', rows=rows, target_field=target_field)


def loading_postgres_continent(dt):
    df = pd.read_parquet(f'{data_dir}/gold/covid_stat/{dt}_covid_statistics.parquet')
    pg_hook = PostgresHook(postgres_conn_id='postgres_localhost')
    rows = [list(row) for row in df.itertuples()]
    target_field = list(df.columns)
    pg_hook.insert_rows(table='covid_statistics_continent', rows=rows, target_field=target_field)


default_args = {
    'owner': 'dmitry',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'email_on_failure': True
}

with DAG(
        dag_id='covid_status',
        start_date=datetime(2022, 3, 7, tzinfo=timezone('Europe/Moscow')),
        schedule_interval='10 13 * * *',
        catchup=True,
        default_args=default_args
) as dag:
    today = "{{ next_execution_date.in_timezone('Europe/Moscow').strftime('%Y-%m-%d') }}"

    # extract_covid_statistics
    PythonOperator(
        task_id='extract_covid_statistics',
        python_callable=extract_covid_statistics,
        op_kwargs={'dt': today}
    )

    # transform_covid_data
    PythonOperator(
        task_id='transform_covid_data',
        python_callable=transform_covid_data,
        op_kwargs={'dt': today}
    )

    # calculations_to_analyst
    PythonOperator(
        task_id='calculations_to_analyst',
        python_callable=calculations_to_analyst,
        op_kwargs={'dt': today}
    )

    # loading_postgres_fact
    PythonOperator(
        task_id='loading_postgres_fact',
        python_callable=loading_postgres_fact,
        op_kwargs={'dt': today}
    )

    # loading_postgres_continent
    PythonOperator(
        task_id='loading_postgres_continent',
        python_callable=loading_postgres_continent,
        op_kwargs={'dt': today}
    )

    t = dag.task_dict
    t['extract_covid_statistics'] >> t['transform_covid_data'] >> \
                                    [t['loading_postgres_fact'], t['calculations_to_analyst']]
    t['calculations_to_analyst'] >> t['loading_postgres_continent']

