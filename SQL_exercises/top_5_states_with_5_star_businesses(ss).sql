-- Top 5 States With 5 Star Businesses

-- Find the top 5 states with the most 5 star businesses. Output the state name along with the number of 5-star businesses and order records by the number of 5-star businesses in descending order. 
-- In case there are ties in the number of businesses, return all the unique states. If two states have the same result, sort them in alphabetical order.
-- https://platform.stratascratch.com/coding/10046-top-5-states-with-5-star-businesses?code_type=1

# yelp_business
# business_id: varchar
# name: varchar
# neighborhood: varchar
# address: varchar
# city: varchar
# state: varchar
# postal_code: varchar
# stars: float
# review_count: int
# is_open: int
# categories: varchar

-- Option 1
with cte as (
select state, count(1) as cnt
from yelp_business
where stars = 5
group by state
order by cnt desc, state)

select * 
from cte 
where cnt in (select cnt from cte order by cnt desc limit 5);

-- Option 2
with cte as (
select state, count(name), rank() over (order by count(name) desc) as rnk
from yelp_business
where stars = 5
group by state)

select *
from cte 
where rnk <= 5;



