# API Gateway
Allows you to create an open door for programs to access AWS resources. It is necessary to set the API Key to protect our URL.

You can create a link URL for each lambda function. After clicking on the link, the Lambda function will be launched.

## Create an API
- Choose Integrations:
Lambda

What will Lambda do: show all S3 Buckets

![image](https://user-images.githubusercontent.com/55916170/162078079-ebea1c8c-f756-4aae-838f-d97b404ec201.png)


- Give the name of the API Gateway: 	TriggerLambdaListS3Buckets
- Сhoice of parameter passing method:
- If we pass the API Key, then POST

![image](https://user-images.githubusercontent.com/55916170/162078991-d40711e7-2238-4a14-af11-a524592a7ba6.png)

- FINISH!
