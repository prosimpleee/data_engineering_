# RDS - Import Database in SQL Server
![Scheme](https://user-images.githubusercontent.com/55916170/162390402-0a0c9902-0e06-4a74-83c2-26a4aabb2472.png)

1. Create S3 Bucket in the same Region as RDS and upload your .bak files 
2. Create new RDS *OptionGroup* with SQLSERVER_BACKUP_RESTORE option 
3. Apply this *OptionGroup* to your RDS INSTEAD of default *OptionGroup* 
4. Connect to RDS, open NewQuery, execude stored procedure:
![image](https://user-images.githubusercontent.com/55916170/162391641-0188b8c5-a283-4a36-9695-3943c027c9c4.png)

## Steps:
1. Create S3 Bucket 

![image](https://user-images.githubusercontent.com/55916170/162393049-13ad3e05-4e34-4ead-b1a7-6dbed5616867.png)

2. Create *OptionGroup* 

![image](https://user-images.githubusercontent.com/55916170/162394012-0d97b0e1-75d9-43ce-97b3-e2a8f79fde17.png)

3. Add OptionGroup to your RDS

![image](https://user-images.githubusercontent.com/55916170/162394685-67496d78-babf-4678-8622-9f0fd7a0b50a.png)

IAM role - Yes (permission read/write)

![image](https://user-images.githubusercontent.com/55916170/162395026-eaba7e35-216e-41ab-acc4-fd042d049800.png)

- Scheduling == Immediately

![image](https://user-images.githubusercontent.com/55916170/162395274-fc314201-f5a8-4e55-b3c3-bf4b309cd3bd.png)

Go to Databases -> Modify -> Database Options -> OptionGroup -> Сhange to our group (msssql-option-backup) -> Apply Immediately

4. Upload your .bak to S3

5. Go to MSSQL -> NewQuery 
```mssql
exec msdb.dbo.rds_restore_database
@restore_db_name='AdventureWorks',
@s3_arn_to_restore_from='arn:aws:s3:::mssql-buckup-prosimplee/AdventureWorks2016.bak';
```
```mssql
exec msdb.dbo.rds_task_status
```
lifecycle = IN_PROGRESS -> lifecycle = SUCCESS
