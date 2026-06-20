"""add model name and storage path

Revision ID: 72569424f1e5
Revises: 65932b60d32b
Create Date: 2026-06-18 19:36:35.238883

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72569424f1e5'
down_revision: Union[str, Sequence[str], None] = '65932b60d32b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(
        "generated_artifacts",
        sa.Column(
            "model_name",
            sa.String(length=500),
            nullable=True
        )
    )

    op.add_column(
        "generated_artifacts",
        sa.Column(
            "storage_path",
            sa.String(length=1000),
            nullable=True
        )
    )

def downgrade():

    op.drop_column(
        "generated_artifacts",
        "storage_path"
    )

    op.drop_column(
        "generated_artifacts",
        "model_name"
    )