from pathlib import Path

from app.services.sp_normalizer_service import (
    SPNormalizerService
)

from app.services.logic_classifier_service import (
    LogicClassifierService
)

from app.services.business_statement_parser import (
    BusinessStatementParser
)

sql = Path(
    "tests/parser/complex_sp.sql"
).read_text()

normalized = (
    SPNormalizerService.normalize(
        sql
    )
)

classified = (
    LogicClassifierService.classify(
        normalized
    )
)

for statement in classified[
    "business_statements"
]:

    print("=" * 80)
    print(statement)
    print()
    
    print("TARGET TABLES")
    print(
        BusinessStatementParser.extract_target_tables(
            statement
        )
    )

    print()

    print("SOURCE TABLES")
    print(
        BusinessStatementParser.extract_source_tables(
            statement
        )
    )
