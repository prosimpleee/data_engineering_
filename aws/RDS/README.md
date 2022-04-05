# RDS - Relation Database

## Public or Private Endpoint
This is the url of the database with/without internet access.

Example:

If you have an application and this application has a table of records (Leaders Dashboard), you make public access to the database.

## Read Replica
- Creates a copy of the database and makes it readable.

## Backup Snapshots Automatic
- Makes snapshots automatic (every day/ every month). Every day will take a snapshot of your database.

## Backup Snapshots Manual
- Makes snapshots manual. Snapshots are not deleted when the database is deleted.

## Multi-AZ (Yes/No)
- Creates an additional example in another availability zone. 

# Steps:
## 1) Database selection:
 
![image](https://user-images.githubusercontent.com/55916170/161764143-6873c395-4e35-4992-941a-c3885fd63e2d.png)

## 2) Database version selection:
 
![image](https://user-images.githubusercontent.com/55916170/161764470-ad2b199e-ba73-4d02-8239-77254e6df72a.png)

## 3) Database name selection:
 
![image](https://user-images.githubusercontent.com/55916170/161765788-083c1553-8c32-4279-8262-59ae69cac520.png)

## 4) Database size selection:

![image](https://user-images.githubusercontent.com/55916170/161764689-f779acec-0bd5-44c1-9e7c-5774f1188634.png)
You can always change size.

## 5) Selecting the drive on which the database will run:
 
![image](https://user-images.githubusercontent.com/55916170/161765401-ad08e92f-928a-477c-83be-950529d05ec2.png)

## 6) Selecting the network on which to run the database:

![image](https://user-images.githubusercontent.com/55916170/161766357-a437d120-9020-4a72-8289-b680f46d94af.png)

## 7) Public or Not Public database:

![image](https://user-images.githubusercontent.com/55916170/161766592-159b541a-2771-498c-b8cf-734b43cf39fe.png)

## 8) Select a VPC security group:

![image](https://user-images.githubusercontent.com/55916170/161766985-1ce768cd-7a0c-4126-9a11-31eb55cb036b.png)

## 9) Selecting Backup retencion period:

![image](https://user-images.githubusercontent.com/55916170/161768523-f86729f9-43a1-48c6-9d1d-4062aba57f83.png)

Selecting the time at which the backup will take place. If you choose 7 days, then on day 8 it will erase the old backup.

## 10) Whether to give the opportunity to make Amazon the simplest database updates?
![image](https://user-images.githubusercontent.com/55916170/161769269-88bc26bf-b0b2-40a1-bb3c-e4b8685608b7.png)

## 11) Finish:
![image](https://user-images.githubusercontent.com/55916170/161769722-8b3536e1-05ac-404d-ad47-ca4015cf0aea.png)

## Connect MSSQL
Server Name -> (UI: Connect - Endpoint)

Login -> Your Master username

Password == Password






