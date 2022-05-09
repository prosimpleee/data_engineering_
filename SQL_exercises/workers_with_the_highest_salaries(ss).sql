# Workers With The Highest Salaries
# Find the titles of workers that earn the highest salary. Output the highest-paid title or multiple titles that share the highest salary.
# https://platform.stratascratch.com/coding/10353-workers-with-the-highest-salaries?code_type=1

# worker
# worker_id: int
# first_name: varchar
# last_name: varchar
# salary: int
# joining_date: datetime
# department: varchar

# title
# worker_ref_id: int
# worker_title: varchar
# affected_from: datetime

with cte as (
select worker_title , department, max(salary) as salary 
from worker w join title t on w.worker_id = t.worker_ref_id 
group by worker_title, department)

select *
from cte 
where salary = (select max(salary) from worker)