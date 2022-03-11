***DW Architecture***

Data Warehouse is primarily optimized for reporting and analytics.
What problems may arise if we start writing analytical queries and building reports based on OLTP?

- Several heterogeneous data sources (CRM, another DB, Files).
- Inconsistent data (intermediate results after query execution).
- Data accumulates extremely fast (a lot of data - the database is running slowly).
- Blocking (writer blocks reader).
- Highly normalized tables in OLTP (many tables - many connections - complex structure).
- Data Quality (London, Lnd, LONDON- different cities in Group By clause).
- Issuing access to different tables for the user.

