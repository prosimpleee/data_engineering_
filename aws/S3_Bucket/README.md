# S3 - Simple Storage Service
Amazon guarantees: 99.99% availability, 99.99999999999% durability

Data in S3 is written to different places

## S3 is used for:
- backup & recovery (backup database, servers, disks)
- data archiving (glacier)
- big data analytics
- web sites(without php, java or smth else)

Maximum file size 5TB (special method);
Max file size per 1 put 160GB.

## File/Object Storage Types
- Amazon s3 Standard (for frequently used files, 2 data centers for data storage)
- Amazon s3 Standard - Infrequent Access (for files that are not needed very often, 2 data centers for data storage)
- Reduced Redundancy Storage (very cheap, for files that are easy to restore, 1 data center for data storage)
- Amazon Glacier (for archived data, slow file access)
