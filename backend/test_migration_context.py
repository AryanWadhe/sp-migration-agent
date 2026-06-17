from pathlib import Path

from app.services.migration_context_service import (
    MigrationContextService
)

sql = Path(
    "tests/parser/complex_sp.sql"
).read_text()

context = (
    MigrationContextService.build_context(
        sql
    )
)

print(context)