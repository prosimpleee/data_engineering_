-- Average Salaries
-- Compare each employee's salary with the average salary of the corresponding department.
-- Output the department, first name, and salary of employees along with the average salary of that department.
-- https://platform.stratascratch.com/coding/9917-average-salaries?code_type=1

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


select first_name, 
       last_name, 
       department, 
       salary, 
       avg(salary) over (partition by department) as avg_salary_department
from employee

