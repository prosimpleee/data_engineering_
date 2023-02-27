-- Most Profitable Companies
-- Find the 3 most profitable companies in the entire world.
-- Output the result along with the corresponding company name.
-- Sort the result based on profits in descending order.
-- https://platform.stratascratch.com/coding/10354-most-profitable-companies

# forbes_global_2010_2014
# company: varchar
# sector: varchar
# industry: varchar
# continent: varchar
# country: varchar
# marketvalue: float
# sales: float
# profits: float
# assets: float
# rank: int
# forbeswebpage: varchar

with cte as (
select company, 
	   profits,
	   rank() over (order by profits desc) as rnk
from forbes_global_2010_2014)

select company, profits
from cte 
where rnk < 4
