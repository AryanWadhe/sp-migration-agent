from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base


class ArtifactType(str, Enum):
    STORED_PROCEDURE = "stored_procedure"
    VIEW = "view"
    FUNCTION = "function"
    TABLE = "table"
    DDL = "ddl"
    SQL_FILE = "sql_file"


class ArtifactStatus(str, Enum):
    UPLOADED = "uploaded"
    PARSING = "parsing"
    PARSED = "parsed"
    GENERATING = "generating"
    GENERATED = "generated"
    FAILED = "failed"


class Artifact(Base):
    __tablename__ = "artifacts"

    artifact_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.project_id"),
        nullable=False
    )

    file_name: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    artifact_type: Mapped[ArtifactType] = mapped_column(
        SqlEnum(ArtifactType),
        nullable=False
    )

    status: Mapped[ArtifactStatus] = mapped_column(
        SqlEnum(ArtifactStatus),
        nullable=False,
        default=ArtifactStatus.UPLOADED
    )

    original_content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    content_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )

    storage_path: Mapped[str | None] = mapped_column(
        String(1000),
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