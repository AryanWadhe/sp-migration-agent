class DBTGenerationService:

    @staticmethod
    def generate(
        migration_context: dict
    ) -> dict:

        source_tables = migration_context.get(
            "source_tables",
            []
        )

        target_tables = migration_context.get(
            "target_tables",
            []
        )

        if not source_tables:

            return {
                "target_model": "unknown_model",
                "dbt_sql": "-- No source tables detected"
            }

        target_model = (
            target_tables[0]
            if target_tables
            else "generated_model"
        )

        ctes = []

        for table in source_tables:

            ctes.append(
f"""
{table}_source as (

    select *
    from {{{{ source('legacy', '{table}') }}}}

)
"""
            )

        dbt_sql = (
            "with\n"
            + ",\n".join(ctes)
            + "\n\nselect *\nfrom "
            + f"{source_tables[0]}_source"
        )

        return {
            "target_model": target_model,
            "dbt_sql": dbt_sql
        }