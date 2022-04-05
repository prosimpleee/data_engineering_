# AWS Lambda 
AWS Lambda allows you to run code without running servers. Program code runs on elastic power computers.

Lambda works on: Python, Node.js, Java, C#.

You can run a Lambda function on:
- AWS Management Console
- AWS CLI
- API Gateway (creates a link URL that launches a Lambda function)
- Run on events

## Сreate a lambda function to output all buckets from S3:
1. I create a role in the IAM to read the S3 buckets for the Lambda.
![image](https://user-images.githubusercontent.com/55916170/161852515-99927939-a456-43f2-abb5-eec3d3caf714.png)

2. The name of the function and in what language the function will be written:
![image](https://user-images.githubusercontent.com/55916170/161852936-d68cda81-bd6c-42bc-945a-6c23aca7fa33.png)

3. What can this function do in aws account? (Read Only S3)
![image](https://user-images.githubusercontent.com/55916170/161853168-183867ac-a109-4550-be48-f9a4afb7f86d.png)

