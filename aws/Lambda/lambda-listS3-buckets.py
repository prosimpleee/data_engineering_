import json
import boto3, os

def lambda_handler(event, context):
    mys3 = boto3.client('s3')
    try: 
        response = mys3.list_buckets()
        dictinary = [{'bucket_name' : bucket['Name'],
                     'created_date' : bucket['CreationDate'].strftime('%Y-%m-%d')}
                     for bucket in response['Buckets']]
        return dictinary
    except:
        return ('Error!')