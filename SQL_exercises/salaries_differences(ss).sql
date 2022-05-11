-- Salaries Differences
-- Write a query that calculates the difference between the highest salaries found in the marketing and engineering departments. Output just the absolute difference in salaries.
-- https://platform.stratascratch.com/coding/10308-salaries-differences?code_type=1

# db_employee
# id: int
# first_name: varchar
# last_name: varchar
# item: varchar
# salary: int
# department_id: int
# email:datetime

# db_dept
# id: int
# department: varchar


select (select max(salary) 
        from db_employee
        where department_id = (select id
                              from db_dept
                              where department = 'marketing')
                                                             ) - (select max(salary) 
                                                                  from db_employee
                                                                  where department_id = (select id
                                                                  from db_dept
                                                                  where department = 'engineering')
                                                                  ) as  difference