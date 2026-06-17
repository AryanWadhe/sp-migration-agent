import sqlglot
from sqlglot import exp


class ParserService:

    @staticmethod
    def analyze_sql(
        sql_text: str
    ) -> dict:

        result = {
        "source_tables": [],
        "target_tables": [],
        "views": [],
        "functions": [],
        "joins": [],
        "filters": [],
        "aggregations": []
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