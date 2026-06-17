from app.services.business_statement_parser import (
    BusinessStatementParser
)

from app.services.logic_classifier_service import (
    LogicClassifierService
)

from app.services.sp_normalizer_service import (
    SPNormalizerService
)


class MigrationContextService:

    @staticmethod
    def build_context(
        sql_text: str
    ) -> dict:

        normalized = (
            SPNormalizerService.normalize(
                sql_text
            )
        )

        classified = (
            LogicClassifierService.classify(
                normalized
            )
        )

        source_tables = set()
        target_tables = set()

        for statement in classified[
            "business_statements"
        ]:

            source_tables.update(
                BusinessStatementParser.extract_source_tables(
                    statement
                )
            )

            target_tables.update(
                BusinessStatementParser.extract_target_tables(
                    statement
                )
            )

        return {
            "source_tables": sorted(
                list(source_tables)
            ),
            "target_tables": sorted(
                list(target_tables)
            )
        }