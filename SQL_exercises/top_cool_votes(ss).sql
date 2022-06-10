-- Top Cool Votes
-- Find the review_text that received the highest number of  'cool' votes.
-- Output the business name along with the review text with the highest numbef of 'cool' votes.
-- https://platform.stratascratch.com/coding/10060-top-cool-votes?code_type=1

# yelp_reviews
# business_name: varchar
# review_id: varchar
# user_id: varchar
# stars: varchar
# review_date: datetime
# review_text: varchar
# funny: int
# useful: int
# cool: int

-- Soltion 1:
select business_name,
       review_text
from yelp_reviews
where cool = (select max(cool)
			  from yelp_reviews)

-- Soltion 2:
with cte as (
select business_name,
	   review_text, 
	   sum(cool) as cnt 
from yelp_reviews
group by 1, 2)

select business_name,
	   review_text, 
	   cnt
from cte
where cnt = (select max(cnt) from cte)