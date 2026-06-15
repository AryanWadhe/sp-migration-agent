from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base


class AnalysisType(str, Enum):
    PARSER = "parser"
    DEPENDENCY = "dependency"
    DBT_GENERATION = "dbt_generation"
    VALIDATION = "validation"


class AnalysisStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    analysis_run_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    artifact_id: Mapped[int] = mapped_column(
        ForeignKey("artifacts.artifact_id"),
        nullable=False
    )

    analysis_type: Mapped[AnalysisType] = mapped_column(
        SqlEnum(AnalysisType),
        nullable=False
    )

    status: Mapped[AnalysisStatus] = mapped_column(
        SqlEnum(AnalysisStatus),
        nullable=False,
        default=AnalysisStatus.PENDING
    )

    result_json: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )