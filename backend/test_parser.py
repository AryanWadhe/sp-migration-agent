from app.services.parser_service import (
    ParserService
)

sql = """
SELECT *
FROM employee e
INNER JOIN labor l
    ON e.id = l.employee_id
"""

result = (
    ParserService.analyze_sql(
        sql
    )
)

print(result)