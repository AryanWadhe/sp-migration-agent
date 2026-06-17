CREATE PROCEDURE usp_load_fact_labor

AS

BEGIN

SET NOCOUNT ON;

INSERT INTO audit_log
VALUES(GETDATE());

DELETE FROM stg_labor;

INSERT INTO fact_labor

SELECT
    e.employee_id,
    SUM(l.hours_worked)
FROM employee e
INNER JOIN labor l
    ON e.employee_id = l.employee_id
GROUP BY e.employee_id;

END