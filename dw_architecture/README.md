# DWH Architecture

Data Warehouse is primarily optimized for reporting and analytics.

## What problems may arise if we start writing analytical queries and building reports based on OLTP?

- Several heterogeneous data sources (CRM, another DB, Files).
- Inconsistent data (intermediate results after query execution).
- Data accumulates extremely fast (a lot of data - the database is running slowly).
- Blocking (writer blocks reader).
- Highly normalized tables in OLTP (many tables - many connections - complex structure).
- Data Quality (London, Lnd, LONDON- different cities in Group By clause).
- Issuing access to different tables for the user.

![architecture](https://user-images.githubusercontent.com/55916170/157976157-e4ffdc66-8581-4a6e-8b68-a132ddb30a1d.png)

## ODS Layer
![image](https://user-images.githubusercontent.com/55916170/163778599-751c74c7-cecf-4e5a-9d89-e98bb6f69fa2.png)
- ODS layer is convenient to use to check the data received in staging, as a rule, the check is performed by the number of rows.

