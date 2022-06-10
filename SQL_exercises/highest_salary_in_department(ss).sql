-- Highest Salary In Department
-- Find the employee with the highest salary per department.
-- Output the department name, employee's first name along with the corresponding salary.
-- https://platform.stratascratch.com/coding/9897-highest-salary-in-department?code_type=1

# employee
# id: int
# first_name: varchar
# last_name: varchar
# age: int
# sex: varchar
# employee_title: varchar
# department: varchar
# salary: int
# target: int
# bonus: int
# email: varchar
# city: varchar
# address: varchar
# manager_id: int

-- Soltion 1:
with cte as(
select department, 
	   first_name, 
	   salary, 
	   rank() over(partition by department order by salary desc) as rnk
from employee
group by 1, 2, 3)

select department, 
	   first_name, 
	   salary
from cte 
where rnk = 1
