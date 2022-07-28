
## Question 3. Count records:

-- Answer: cnt_trips = 53024
```sql
select count(1) as cnt_trips
from yellow_taxi_data
where extract('month' from tpep_pickup_datetime) = 1 and extract('day' from tpep_pickup_datetime) = 15
```

## Question 4. Largest tip for each day:

-- Answer: date = "2021-01-20" & tip_amount = 1140.44
```sql
select tpep_pickup_datetime::date, max(tip_amount) as tip_amount
from yellow_taxi_data
group by tpep_pickup_datetime::date
order by tip_amount desc
limit 1
```

