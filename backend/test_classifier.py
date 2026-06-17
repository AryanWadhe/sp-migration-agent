from pathlib import Path

from app.services.sp_normalizer_service import (
    SPNormalizerService
)

from app.services.logic_classifier_service import (
    LogicClassifierService
)

sql = Path(
    "tests/parser/complex_sp.sql"
).read_text()

normalized = (
    SPNormalizerService.normalize(
        sql
    )
)

result = (
    LogicClassifierService.classify(
        normalized
    )
)

print("=" * 80)
print("BUSINESS")
print("=" * 80)

print(
    result["business_sql"]
)

print()

print("=" * 80)
print("SYSTEM")
print("=" * 80)

print(
    result["system_sql"]
)

print()

print("=" * 80)
print("ORCHESTRATION")
print("=" * 80)

print(
    result["orchestration_sql"]
)