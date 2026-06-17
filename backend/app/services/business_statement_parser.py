import sqlglot
from sqlglot import exp


class BusinessStatementParser:

    @staticmethod
    def extract_target_tables(
        sql_text: str
    ) -> list[str]:

        targets = set()

        try:

            parsed = sqlglot.parse_one(
                sql_text
            )

            if isinstance(
                parsed,
                exp.Insert
            ):

                targets.add(
                    parsed.this.name
                )

        except Exception:
            pass

        return sorted(
            list(targets)
        )

    @staticmethod
    def extract_source_tables(
        sql_text: str
    ) -> list[str]:

        targets = set(
            BusinessStatementParser.extract_target_tables(
                sql_text
            )
        )

        all_tables = set()

        try:

            parsed = sqlglot.parse_one(
                sql_text
            )

            for table in parsed.find_all(
                exp.Table
            ):

                all_tables.add(
                    table.name
                )

        except Exception:
            pass

        sources = (
            all_tables - targets
        )

        return sorted(
            list(sources)
        )