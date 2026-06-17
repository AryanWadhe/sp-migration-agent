from pydantic import BaseModel


class UploadGenerateResponse(
    BaseModel
):
    artifact_id: int
    generated_artifact_id: int
    target_model: str
    dbt_sql: str