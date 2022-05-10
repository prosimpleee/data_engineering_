import json
import boto3
import requests
import time
from botocore.client import Config
from datetime import date
import pandas as pd
from io import StringIO
import os

TOKEN_API = os.environ['MY_API_KEY']
AWS_ACCESS_KEY = os.environ['MY_AWS_KEY']
AWS_SECRET_ACCESS_KEY = os.environ['MY_AWS_SECRET_KEY']


def extract_matches_data(TOKEN_API, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY):
    url = "https://serie-a2.p.rapidapi.com/match_schedule/2022/34"

    headers = {
        "X-RapidAPI-Host": "serie-a2.p.rapidapi.com",
        "X-RapidAPI-Key": TOKEN_API
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    json_object = data
    bucket_name = "seriaa-matches"
    file_name = "bronze_data/seriaa_matches_" + str(date.today()) + ".json"
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


extract_matches_data(TOKEN_API, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)


def stat_mathces(AWS_ACCESS_KEY,AWS_SECRET_ACCESS_KEY):
    s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    content_object = s3.Object('seriaa-matches', "bronze_data/seriaa_matches_" + str(date.today()) + ".json")
    file_content = content_object.get()['Body'].read().decode('utf-8')
    data = json.loads(file_content)

    matches = [{'home_team': i['Home Team'],
                'home_score': i['Home Score'],
                'away_score': i['Away Score'],
                'away_team': i['Away Team'],
                'match_day': i['Timestamp'],
                'stadion': ' '.join(i['Venue'].split()[1:-1]).title()} for i in data['data']]
    df = pd.DataFrame(matches)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, sep='|')
    bucket_name = "seriaa-matches"
    file_name = "gold_data/seriaa_matches_" + str(date.today()) + ".csv"
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

stat_mathces(AWS_ACCESS_KEY,AWS_SECRET_ACCESS_KEY)