-- Finding User Purchases
-- Write a query that'll identify returning active users. A returning active user is a user that has made a second purchase within 7 days of any other of their purchases. 
-- Output a list of user_ids of these returning active users.
-- https://platform.stratascratch.com/coding/10322-finding-user-purchases?code_type=1

# amazon_transactions
# id: int
# user_id: int
# item: varchar
# created_at: datetime
# revenue: int

with cte as(
select  user_id, created_at,
        lead(created_at) over(partition by user_id order by created_at) as next_purc
from amazon_transactions
order by user_id, created_at)

select user_id
from cte 
where datediff(next_purc, created_at) <= 7
group by user_id
