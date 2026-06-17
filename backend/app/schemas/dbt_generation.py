from pydantic import BaseModel


class DBTGenerationResponse(
    BaseModel
):
    generated_artifact_id: int
    target_model: str
    dbt_sql: str