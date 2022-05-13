-- Finding Updated Records
-- We have a table with employees and their salaries, however, some of the records are old and contain outdated salary information. Find the current salary of each employee assuming that salaries increase each year. 
-- Output their id, first name, last name, department ID, and current salary. Order your list by employee ID in ascending order.
-- https://platform.stratascratch.com/coding/10299-finding-updated-records?code_type=1

# ms_employee_salary
# id: int
# first_name: varchar
# last_name: varchar
# salary: int
# department_id: int

-- Option 1
select id, first_name, last_name, department_id, max(salary) as salary
from ms_employee_salary
group by id, first_name, last_name, department_id
order by id 

-- Option 2
select distinct id, first_name, last_name, department_id, 	
       first_value(salary) over (partition by first_name, last_name order by salary desc) as salary 
from ms_employee_salary
order by id 




