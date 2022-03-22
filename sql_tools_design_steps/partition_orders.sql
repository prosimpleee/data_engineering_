-- 1 Step: Create Partition Function
CREATE PARTITION FUNCTION PartDate (datetime)
	AS 
		RANGE FOR VALUES (
						'2014-1-1',
						'2013-1-1',
						'2012-1-1',
						'2011-1-1'
						)


-- 2 Step: Create Partition Schema
CREATE PARTITION SCHEME DateScheme 
	AS
		PARTITION PartDate TO (
						'PRIMARY',
						'PRIMARY',
						'PRIMARY',
						'PRIMARY',
						'PRIMARY'
								)

-- 3 Step: Create Fact Table on DateScheme
