# IAM Service

The service allows providing users/groups of users with access to AWS resources.

## Create Group & Add User
We create a group, select the necessary permissions and add users. Permissions can be issued for various Amazon services depending on business requirements. Starting from a microservice(EC2, S3, RDS, Redshift..) and ending with full access to Amazon services.
![Create Group & Add User](https://user-images.githubusercontent.com/55916170/161327082-d17a8818-3f70-4577-be96-c08ec78b0e7e.jpg)
![Create Group & Add User](https://github.com/prosimpleee/data_engineering_/blob/main/aws/IAM_Service/iam_service.pdf)

## Usage via aws cli:
- Install Python.
- Install AWS CLI
```python
pip install awscli
```
Command Line:
```windows
aws configure
```
- AWS Access Key ID: enter access key id

- AWS Secret Access Key ID: enter secret access key id

- Default region name (amazon default region): 'like:' eu-central-1

## Example Run: 
```windows
aws ec2 describe-instances
```
```windows
aws ec2 describe-regions
```
