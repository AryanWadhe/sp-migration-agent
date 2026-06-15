import json
from datetime import datetime

from app.models.analysis_run import (
    AnalysisRun,
    AnalysisStatus,
    AnalysisType
)

from app.repositories.analysis_run_repository import (
    AnalysisRunRepository
)

from app.repositories.artifact_repository import (
    ArtifactRepository
)

from app.services.parser_service import (
    ParserService
)


class ParserAnalysisService:

    @staticmethod
    def analyze_artifact(
        db,
        artifact_id: int
    ):

        artifact = (
            ArtifactRepository.get_by_id(
                db,
                artifact_id
            )
        )

        if not artifact:
            raise ValueError(
                "Artifact not found"
            )

        result = (
            ParserService.analyze_sql(
                artifact.original_content
            )
        )

        analysis_run = AnalysisRun(
            artifact_id=artifact.artifact_id,
            analysis_type=AnalysisType.PARSER,
            status=AnalysisStatus.COMPLETED,
            result_json=json.dumps(
                result,
                indent=2
            ),
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow()
        )

        return (
            AnalysisRunRepository.create(
                db,
                analysis_run
            )
        )