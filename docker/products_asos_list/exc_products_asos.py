import pandas as pd
import boto3
from io import StringIO
import requests
from datetime import date
from botocore.client import Config
import json
import os
import time

TOKEN_API = os.environ['MY_API_KEY']
AWS_ACCESS_KEY = os.environ['MY_AWS_KEY']
AWS_SECRET_ACCESS_KEY = os.environ['MY_AWS_SECRET_KEY']

def extract_products(TOKEN_API, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY):
    url = "https://asos2.p.rapidapi.com/products/v2/list"

    querystring = {"store": "US",
                   "offset": "0",
                   "categoryId": "4209",
                   "limit": "50",
                   "country": "US",
                   "sort": "freshness",
                   "currency": "USD",
                   "sizeSchema": "US",
                   "lang": "en-US"}

    headers = {
        "X-RapidAPI-Host": "asos2.p.rapidapi.com",
        "X-RapidAPI-Key": TOKEN_API
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    json_object = data
    bucket_name = "products-asos-prosimplee"
    file_name = "bronze_data/asos_products_" + str(date.today()) + ".json"
    s3 = boto3.resource('s3',
                        aws_access_key_id=AWS_ACCESS_KEY,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        config=Config(signature_version='s3v4')
                        )
    try:
        s3.Bucket(bucket_name).put_object(Key=file_name, Body=json.dumps(json_object), ACL='public-read')
        print('Success')
    except ValueError:
        print('Failure')
    time.sleep(15)


extract_products(TOKEN_API, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)


def transofrm_data(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY):
    s3 = boto3.resource('s3', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
    content_object = s3.Object('products-asos-prosimplee', "bronze_data/asos_products_" + str(date.today()) + ".json")
    file_content = content_object.get()['Body'].read().decode('utf-8')
    data = json.loads(file_content)
    all_products = [{
        'brand_name': i['brandName'].title(),
        'product_name': i['name'].title(),
        'product_color': i['colour'].title(),
        'product_price': i['price']['current']['text'],
        'image': i['imageUrl']} for i in data['products']]

    df = pd.DataFrame(all_products)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer,sep='|')
    bucket_name = "products-asos-prosimplee"
    file_name = "gold_data/asos_products_" + str(date.today()) + ".csv"
    s3 = boto3.resource('s3',
                        aws_access_key_id=AWS_ACCESS_KEY,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        config=Config(signature_version='s3v4')
                        )
    try:
        s3.Bucket(bucket_name).put_object(Key=file_name, Body=csv_buffer.getvalue(), ACL='public-read')
        print(f"Your {file_name} has been successfully uploaded!")
    except NameError:
        print("Error!!!")


transofrm_data(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)

