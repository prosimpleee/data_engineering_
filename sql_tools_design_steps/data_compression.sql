-- Data Compression:
-- Method Page - for archived data (old partitions).
-- Method Row - for almost new data.
USE db
ALTER TABLE [dbo].[fact.Orders] REBUILD PARTITION = 1 WITH(DATA_COMPRESSION = PAGE )
USE db
ALTER TABLE [dbo].[fact.Orders] REBUILD PARTITION = 2 WITH(DATA_COMPRESSION = PAGE )
USE db
ALTER TABLE [dbo].[fact.Orders] REBUILD PARTITION = 3 WITH(DATA_COMPRESSION = ROW )
USE db
ALTER TABLE [dbo].[fact.Orders] REBUILD PARTITION = 4 WITH(DATA_COMPRESSION = NONE )
USE db
ALTER TABLE [dbo].[fact.Orders] REBUILD PARTITION = 5 WITH(DATA_COMPRESSION = NONE )
