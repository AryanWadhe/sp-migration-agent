from pathlib import Path

from app.services.sp_normalizer_service import (
    SPNormalizerService
)

from app.services.logic_classifier_service import (
    LogicClassifierService
)


sql = Path(
    "tests/parser/complex_sp.sql"
).read_text(
    encoding="utf-8"
)

normalized_sql = (
    SPNormalizerService.normalize(
        sql
    )
)

result = (
    LogicClassifierService.classify(
        normalized_sql
    )
)

print("=" * 80)
print("CLASSIFICATION RESULT")
print("=" * 80)

print()

print("SYSTEM STATEMENTS")
print("-" * 80)

for statement in result[
    "system_statements"
]:
    print(statement)
    print()

print()

print("ORCHESTRATION STATEMENTS")
print("-" * 80)

for statement in result[
    "orchestration_statements"
]:
    print(statement)
    print()

print()

print("BUSINESS STATEMENTS")
print("-" * 80)

for statement in result[
    "business_statements"
]:
    print(statement)
    print()