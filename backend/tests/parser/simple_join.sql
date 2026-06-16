SELECT
    e.employee_id,
    l.hours_worked
FROM employee e
INNER JOIN labor l
    ON e.employee_id = l.employee_id