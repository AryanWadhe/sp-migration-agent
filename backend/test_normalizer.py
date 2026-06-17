from pathlib import Path

from app.services.sp_normalizer_service import (
    SPNormalizerService
)

sql = Path(
    "tests/parser/complex_sp.sql"
).read_text()

normalized = (
    SPNormalizerService.normalize(
        sql
    )
)

print(normalized)