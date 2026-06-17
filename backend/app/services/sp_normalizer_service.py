import re


class SPNormalizerService:

    @staticmethod
    def normalize(
        sql_text: str
    ) -> str:

        sql_text = re.sub(
            r"CREATE\s+PROCEDURE.*?BEGIN",
            "",
            sql_text,
            flags=re.IGNORECASE | re.DOTALL
        )

        sql_text = re.sub(
            r"END\s*$",
            "",
            sql_text,
            flags=re.IGNORECASE
        )

        sql_text = re.sub(
            r"SET\s+NOCOUNT\s+ON\s*;",
            "",
            sql_text,
            flags=re.IGNORECASE
        )

        return sql_text