-- Users By Average Session Time
-- Calculate each user's average session time. 
-- A session is defined as the time difference between a page_load and page_exit. 
-- For simplicity, assume a user has only 1 session per day and if there are multiple of the same events on that day, consider only the latest page_load and earliest page_exit.
-- Output the user_id and their average session time.
-- https://platform.stratascratch.com/coding/10352-users-by-avg-session-time

# facebook_web_log
# user_id: int
# timestamp: datetime
# action varchar

-- Solution 1
with cte as (
select user_id,
       max(timestamp)  FILTER (WHERE action = 'page_load')
            over(partition by user_id, 
                 date(timestamp)) as tm_1,
       min(timestamp) FILTER (WHERE action = 'page_exit')
            over(partition by user_id, 
                 date(timestamp))  as tm_2
from facebook_web_log
where action in ('page_load', 'page_exit'))

select user_id, EXTRACT(epoch FROM avg(tm_2 - tm_1)) as session_minutes  
from cte 
group by 1
having EXTRACT(epoch FROM avg(tm_2 - tm_1)) > 0
order by user_id


