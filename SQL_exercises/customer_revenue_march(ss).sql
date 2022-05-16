-- Customer Revenue In March

-- Calculate the total revenue from each customer in March 2019. 
-- Include only customers who were active in March 2019. 
-- https://platform.stratascratch.com/coding/9782-customer-revenue-in-march?code_type=1

# orders
# id: int
# cust_id: int
# order_date: datetime
# order_details: varchar
# total_order_cost: int

-- Option 1
select cust_id, sum(total_order_cost) as total
from orders
where extract('month' from order_date) = 03 and extract('year' from order_date) = 2019
group by 1
order by total desc

-- Option 2
select cust_id, sum(total_order_cost) as total
from orders
where order_date >= '2019-03-01' and order_date <= '2019-03-31' -- between
group by 1
order by total desc


-- Option 3
with cte as(
select cust_id, total_order_cost
from orders
where extract('month' from order_date) = 03 and extract('year' from order_date) = 2019)

select cust_id, sum(total_order_cost) as total
from cte
group by cust_id
order by total desc

