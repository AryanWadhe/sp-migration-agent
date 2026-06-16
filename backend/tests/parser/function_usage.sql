SELECT
    employee_id,
    dbo.fn_calculate_bonus(employee_id)
FROM employee