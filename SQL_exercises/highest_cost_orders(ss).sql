-- Highest Cost Orders
-- Find the customer with the highest daily total order cost between 2019-02-01 to 2019-05-01. If customer had more than one order on a certain day, sum the order costs on daily basis. Output customer's first name, total cost of their items, and the date.
-- For simplicity, you can assume that every first name in the dataset is unique. 
-- https://platform.stratascratch.com/coding/9915-highest-cost-orders?code_type=1

# customers
# id: int
# first_name: varchar
# last_name: varchar
# city: varchar
# address: varchar
# phone_number: varchar

# orders
# id: int
# cust_id: int
# order_date: datetime
# order_details: varchar
# total_order_cost: int

with cte as (
select first_name, 
       last_name, 
       order_date, 
       sum(total_order_cost) as total
from customers c join orders o on c.id = o.cust_id 
                               and (order_date between '2019-02-01' and '2019-05-01')
group by first_name, last_name, order_date)

select first_name, 
       order_date, 
       total
from cte 
where total = (select max(total) from cte)



