from pathlib import Path

from app.services.parser_service import (
    ParserService
)


PARSER_TEST_FOLDER = Path(
    "tests/parser"
)


for sql_file in (
    PARSER_TEST_FOLDER.glob("*.sql")
):

    print("=" * 80)

    print(
        f"FILE: {sql_file.name}"
    )

    sql_text = sql_file.read_text(
        encoding="utf-8"
    )

    result = (
        ParserService.analyze_sql(
            sql_text
        )
    )

    print(result)

    print()