from pathlib import Path

from app.services.sp_normalizer_service import (
    SPNormalizerService
)

from app.services.sql_statement_splitter import (
    SQLStatementSplitter
)

sql = Path(
    "tests/parser/complex_sp.sql"
).read_text()

normalized = (
    SPNormalizerService.normalize(
        sql
    )
)

statements = (
    SQLStatementSplitter.split(
        normalized
    )
)

for idx, statement in enumerate(
    statements,
    start=1
):
    print("=" * 80)
    print(f"STATEMENT {idx}")
    print("=" * 80)

    print(statement)

    print()