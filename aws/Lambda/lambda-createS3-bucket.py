import json
import boto3, os
import time

AWS_DEFAULT_REGION = "eu-west-1"  # Region where Lambda running
os.environ['AWS_DEFAULT_REGION'] = AWS_DEFAULT_REGION


bucketname = 'lambda-prosimplee-me-git-' + str(time.strftime('%H-%M-%S'))

def lambda_handler(event, context):
    myS3 = boto3.resource('s3')
    try:
        results = myS3.create_bucket(
            Bucket=bucketname,
            CreateBucketConfiguration={'LocationConstraint': AWS_DEFAULT_REGION}
        )
        return ('Bucket Created Successfully: ' + str(results))
    except:
        return ('Error!')