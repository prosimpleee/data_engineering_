
-- Host Popularity Rental Prices
-- You’re given a table of rental property searches by users. The table consists of search results and outputs host information for searchers. Find the minimum, average, maximum rental prices for each host’s popularity rating. 
-- The host’s popularity rating is defined as below:
--    0 reviews: New
--    1 to 5 reviews: Rising
--    6 to 15 reviews: Trending Up
--    16 to 40 reviews: Popular
--    more than 40 reviews: Hot

-- Tip: The id column in the table refers to the search ID. You'll need to create your own host_id by concating price, room_type, host_since, zipcode, and number_of_reviews.
-- Output host popularity rating and their minimum, average and maximum rental prices.
-- https://platform.stratascratch.com/coding/9632-host-popularity-rental-prices?code_type=1

# airbnb_host_searches
# id: int
# price: float
# property_type: varchar
# room_type: varchar
# amenities: varchar
# accommodates: int
# bathrooms: int
# bed_type: varchar
# cancellation_policy: varchar
# cleaning_fee: bool
# city: varchar
# host_identity_verified: varchar
# host_response_rate: varchar
# host_since: datetime
# neighbourhood: varchar
# number_of_reviews: int
# review_scores_rating: float
# zipcode: int
# bedrooms: int
# beds: int


with cte as (
select distinct concat(price, room_type, host_since, zipcode, number_of_reviews) as host_id,
        price,
        number_of_reviews 
from airbnb_host_searches)

select case when number_of_reviews = 0 then 'New'
            when number_of_reviews < 6 then 'Rising' 
            when number_of_reviews < 16 then 'Trending Up'
            when number_of_reviews < 41 then 'Popular'
            else 'Hot' end as reviews,
       min(price) as min_price,
       avg(price) as avg_price,
       max(price) as max_price
from cte 
group by 1
