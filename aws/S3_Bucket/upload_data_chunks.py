import time
from io import StringIO
import pandas as pd
from botocore.client import Config
import boto3

# Our Local File
with open('Sample - Superstore.csv', 'r') as csv_file:
    df = pd.read_csv(csv_file, parse_dates=['Order Date'])
    order_month_year = df['Order Date'].dt.to_period('M').unique()
    # Chunk by month & year
    for month_year in order_month_year:
        data = df[(df['Order Date'].dt.to_period('M') == month_year)]
        bucket_name = "superstore-data-prosimplee"
        file_name = str(month_year) + "/silver_data/superstore.csv"
        s3 = boto3.resource('s3',
                            aws_access_key_id='aws_access_key_id',
                            aws_secret_access_key='aws_secret_access_key',
                            config=Config(signature_version='s3v4')
                            )
        csv_buffer = StringIO()
        data.to_csv(csv_buffer, sep=',')
        try:
            s3.Bucket(bucket_name).put_object(Key=file_name, Body=csv_buffer.getvalue(),
                                              ACL='private')
            print('Data was successfully put into S3 bucket!')
        except ValueError:
            print('Put data to S3 bucket: FAILURE!')
