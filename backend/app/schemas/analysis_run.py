from datetime import datetime

from pydantic import BaseModel

from app.models.analysis_run import (
    AnalysisStatus,
    AnalysisType
)


class AnalysisRunResponse(
    BaseModel
):
    analysis_run_id: int
    artifact_id: int
    analysis_type: AnalysisType
    status: AnalysisStatus
    result_json: str | None
    started_at: datetime | None
    completed_at: datetime | None

    class Config:
        from_attributes = True