-- SET STATISTICS IO ON
-- Create Non-Clustered Indexes  
CREATE INDEX IndexCurrency 
	ON [dbo].[dim.Currency] ([CurrencyName]);
		
CREATE INDEX IndexDates 
	ON [dbo].[dim.Calendar] ([YearNumber]) 
		INCLUDE ([MonthNumber],
				 [DayNumber],
				 [MonthText]);

-- Create Filter Indexes
CREATE INDEX IndexPrice 
	ON [dbo].[dim.Product] ([Price]) 
	INCLUDE ([ModelName])
	WHERE [Price] > 1200;

CREATE INDEX IndexQty 
	ON [dbo].[fact.Orders] ([Quantity]) 
	WHERE [Quantity] < 3;


-- Create Columnstore Index
-- Only 1 columnstore index on a table, always scan.
-- MSSQL -> Without Columnstore index: E.S.C = 1,84  ; Logical Reads = 1184							  
-- MSSQL -> With Colunbstore index   : E.S.C = 0,09 ; Logical Reads = 110
SELECT SUM (TotalPriceUsd) AS total_sum, AVG(TotalPriceUsd) AS avg_total_price
FROM [dbo].[fact.Orders]
GROUP BY ProductID

-- How to create columnstore index (MSSQL):
CREATE COLUMNSTORE INDEX column_index 
	ON [dbo].[fact.Orders] (TotalPriceUsd, ProductID)


