# S3 - Simple Storage Service
Amazon guarantees: 99.99% availability, 99.99999999999% durability

Data in S3 is written to different places

## S3 is used for:
- Backup & recovery (backup database, servers, disks)
- Data archiving (glacier)
- Big data analytics
- Web sites(without php, java or smth else)

Maximum file size 5TB (special method);
Max file size per 1 put 160GB.

## File/Object Storage Types
- Amazon s3 Standard (for frequently used files, 2 data centers for data storage)
- Amazon s3 Standard - Infrequent Access (for files that are not needed very often, 2 data centers for data storage)
- Reduced Redundancy Storage (very cheap, for files that are easy to restore, 1 data center for data storage)
- Amazon Glacier (for archived data, slow file access)

## Bucket Versioning
- Enabled/ bucket versioning allows you to select any version of your modified file
- Disabled/ bucket versioning doesn't let you select any version of your modified file
- Bucket Versioning setting can always be changed in: bucket name - properties - Bucket Versioning - Edit

## Tags
- Makes it possible to quickly find a bucket among other buckets

## Server access logging
- Makes it possible to write logging to the bucket

## Make a bucket public & File in Amazon S3
1. Disable all permissions
2. Upload your file
3. Choose Storage class
4. UPLOAD
5. Link: https://testing-bucket-git-prosimplee.s3.eu-west-2.amazonaws.com/test_read_s3.txt

## Now we can read file from S3 bucket (Python)
```python
import boto3
s3_client = boto3.client('s3')
response = s3_client.get_object(Bucket = 'testing-bucket-git-prosimplee', Key = 'test_read_s3.txt')
data = response['Body'].read()
print(data.decode())
```
![image](https://user-images.githubusercontent.com/55916170/161436201-03f4130a-3e50-40c0-a020-913f3ec0b0ae.png)

## Cross-Region Replication S3 Buckets
Be sure to enable "bucket Versioning" in two buckets
1. Create replication name
2. Choose a rule scope
3. Where to copy data? Destination (bucket)
4. Issue a role to write data from the source to the backup
5. Choosing how to store data in a backup
6. Click save
![image](https://user-images.githubusercontent.com/55916170/161440638-88edade8-de7b-4685-94ac-2f35abf91631.png)


