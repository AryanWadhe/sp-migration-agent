from pathlib import Path

from app.services.migration_context_service import (
    MigrationContextService
)

from app.services.dbt_generation_service import (
    DBTGenerationService
)

sql = Path(
    "tests/parser/complex_sp.sql"
).read_text()

context = (
    MigrationContextService.build_context(
        sql
    )
)

result = (
    DBTGenerationService.generate(
        context
    )
)

print(result)