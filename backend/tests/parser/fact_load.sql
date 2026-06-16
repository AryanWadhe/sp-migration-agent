INSERT INTO fact_labor

SELECT
    e.employee_id,
    SUM(l.hours_worked) AS total_hours
FROM employee e
INNER JOIN labor l
    ON e.employee_id = l.employee_id
GROUP BY e.employee_id  