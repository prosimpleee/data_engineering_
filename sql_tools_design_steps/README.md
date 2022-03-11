**Physical aspects of storage:**

Partition:
 - Splits the fact table into sections by date, which can be placed on different filegroups (different disks).

Indexes in the fact table:
- Clustered Index by date_id.
- Non clustered index by important foreign keys.

Indexes in dim Tables:
- Clustered Index by business key.
- Non clustered index by surrogate key and by frequently used attributes (+ include option).
- Filter Indexes - take up little space, convenient for frequently requested attributes, if the query does not get into the index, the query execution speed will decrease.
- ColumnStore Index – is best adapted for aggregation.

Materialized Views - stores the execution of the request instead of the text of the request.

Data Compression:
- Method Page - for archived data (old partitions).
- Method Row - for almost new data.

