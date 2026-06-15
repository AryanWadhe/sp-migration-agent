from sqlalchemy.orm import Session

from app.models.analysis_run import AnalysisRun


class AnalysisRunRepository:

    @staticmethod
    def create(
        db: Session,
        analysis_run: AnalysisRun
    ) -> AnalysisRun:

        db.add(analysis_run)
        db.commit()
        db.refresh(analysis_run)

        return analysis_run