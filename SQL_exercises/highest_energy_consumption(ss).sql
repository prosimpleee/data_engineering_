-- Highest Energy Consumption
-- Find the date with the highest total energy consumption from the Meta/Facebook data centers. Output the date along with the total energy consumption across all data centers.
-- https://platform.stratascratch.com/coding/10064-highest-energy-consumption?code_type=1

# fb_eu_energy
# date: datetime
# consumption: int

# fb_asia_energy
# date: datetime
# consumption: int

# fb_na_energy
# date: datetime
# consumption: int

with cte as (
select date, sum(consumption) as total
from (
    select date,consumption
    from fb_eu_energy
    union all 
    select date,consumption
    from fb_asia_energy
    union all
    select date,consumption
    from fb_na_energy) as table1
group by date)

select date, total 
from cte 
where total = (select max(total) from cte)




