import sqlglot
from sqlglot import exp


class ParserService:

    @staticmethod
    def analyze_sql(
        sql_text: str
    ) -> dict:

        result = {
            "tables": [],
            "views": [],
            "ctes": [],
            "functions": []
        }

        try:

            parsed = sqlglot.parse_one(
                sql_text
            )

            tables = set()

            for table in parsed.find_all(
                exp.Table
            ):
                tables.add(table.name)

            result["tables"] = sorted(
                list(tables)
            )

        except Exception as ex:

            result["error"] = str(ex)

        return result