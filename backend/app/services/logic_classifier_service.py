from app.services.sql_statement_splitter import (
    SQLStatementSplitter
)


class LogicClassifierService:

    SYSTEM_KEYWORDS = [
        "audit",
        "log",
        "error",
        "control"
    ]

    ORCHESTRATION_KEYWORDS = [
        "stg_",
        "stage_",
        "truncate",
        "cleanup"
    ]

    @staticmethod
    def classify(
        sql_text: str
    ) -> dict:

        result = {
            "business_statements": [],
            "system_statements": [],
            "orchestration_statements": []
        }

        statements = (
            SQLStatementSplitter.split(
                sql_text
            )
        )

        for statement in statements:

            lower_statement = (
                statement.lower()
            )

            if any(
                keyword in lower_statement
                for keyword in LogicClassifierService.SYSTEM_KEYWORDS
            ):

                result[
                    "system_statements"
                ].append(statement)

            elif any(
                keyword in lower_statement
                for keyword in LogicClassifierService.ORCHESTRATION_KEYWORDS
            ):

                result[
                    "orchestration_statements"
                ].append(statement)

            else:

                result[
                    "business_statements"
                ].append(statement)

        return result