class SQLStatementSplitter:

    @staticmethod
    def split(
        sql_text: str
    ) -> list[str]:

        statements = []

        for statement in sql_text.split(";"):

            statement = statement.strip()

            if statement:

                statements.append(
                    statement
                )

        return statements