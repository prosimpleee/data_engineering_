-- 1 Step: Create View (Only INNER JOIN, Seek)
CREATE VIEW total_qnt_by_size
	WITH SCHEMABINDING AS
SELECT Size, SUM (OrderQuantity) AS total_qnt, COUNT_BIG(*) AS BIG
	FROM [dbo].[FactInternetSales] f
	JOIN [dbo].[DimProduct] d ON f.ProductKey = d.ProductKey
WHERE Size IS NOT NULL
GROUP BY Size

-- 2 Step: Create Unique index
CREATE UNIQUE CLUSTERED INDEX qnt_size
	ON total_qnt_by_size(Size)

-- 3 Step: Write a query
SELECT * 
FROM total_qnt_by_size
WHERE total_qnt > 130 