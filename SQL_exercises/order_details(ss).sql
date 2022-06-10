-- Order Details
-- Find order details made by Jill and Eva.
-- Consider the Jill and Eva as first names of customers.
-- Output the order date, details and cost along with the first name. Order records based on the customer id in ascending order.
-- https://platform.stratascratch.com/coding/9913-order-details?code_type=1

# customers
# id: int
# first_name: varchar
# last_name: varchar
# city: varchar
# adress: varchar
# phone: varchar

# orders
# id: int
# cust_id: int
# order_date: datetime
# order_details: varchar
# total_order_cost: int

select first_name, 
	   order_date, 
	   order_details, 
	   total_order_cost
from customers c join orders o on c.id = o.cust_id
where first_name in ('Jill', 'Eva')
order by c.id

