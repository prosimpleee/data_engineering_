with cte as (
select company, 
	   profits,
	   rank() over (order by profits desc) as rnk
from forbes_global_2010_2014)

select company, profits
from cte 
where rnk < 4