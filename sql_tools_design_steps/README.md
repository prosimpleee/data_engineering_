# Physical aspects of DWH: #
Requirements for the physical structure of DWH

## Partition Scheme:
```sql
-- 1 Step:
CREATE PARTITION FUNCTION PartDate (column_type)
   AS 
     RANGE FOR VALUES (
                      'board_1',
                      'board_2',
                      'board_3'
                                );
-- 2 Step:
CREATE PARTITION SCHEME scheme_name 
   AS
     PARTITION PartDate TO (
                      'filegroup_1',
                      'filegroup_2',
                      'filegroup_3',
                      'filegroup_4'
                                  );
```
 - Partition allows you to conveniently transfer data for the desired day/week/month or year.
 - Splits the fact table into sections by date, which can be placed on different filegroups (different disks).
 
 [Partition Function & Scheme](https://github.com/prosimpleee/data_engineering_/blob/main/sql_tools_design_steps/partition_orders.sql)
 
## Indexes in the fact table:
- Clustered Index by date_id.
- Non clustered index by important foreign keys.

[Clustered & Non Clustered & ColumnStore Indexes](https://github.com/prosimpleee/data_engineering_/blob/main/sql_tools_design_steps/indexes_orders.sql)

## Indexes in dim Tables:
- Clustered Index by business key.
- Non clustered index by surrogate key and by frequently used attributes (+ include option).
- Filter Indexes - take up little space, convenient for frequently requested attributes, if the query does not get into the index, the query execution speed will decrease.
- ColumnStore Index – is best adapted for aggregation.

## Materialized Views:
- Stores the execution of the request instead of the text of the request.

[Materialized View](https://github.com/prosimpleee/data_engineering_/blob/main/sql_tools_design_steps/materialized_view.sql)

## Data Compression:
- Method Page - for archived data (old partitions).
- Method Row - for almost new data.

[Data Compression](https://github.com/prosimpleee/data_engineering_/blob/main/sql_tools_design_steps/data_compression.sql)
