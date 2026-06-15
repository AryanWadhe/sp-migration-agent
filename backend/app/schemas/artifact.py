from datetime import datetime

from pydantic import BaseModel

from app.models.artifact import ArtifactStatus
from app.models.artifact import ArtifactType


class ArtifactCreate(BaseModel):
    project_id: int
    file_name: str
    artifact_type: ArtifactType
    original_content: str


class ArtifactResponse(BaseModel):
    artifact_id: int
    project_id: int
    file_name: str
    artifact_type: ArtifactType
    status: ArtifactStatus
    file_size: int
    content_hash: str
    storage_path: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True