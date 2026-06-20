from datetime import datetime

from pydantic import BaseModel


class GeneratedArtifactResponse(
    BaseModel
):

    generated_artifact_id: int

    artifact_id: int

    artifact_type: str

    model_name: str | None = None

    storage_path: str | None = None

    content: str

    created_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True