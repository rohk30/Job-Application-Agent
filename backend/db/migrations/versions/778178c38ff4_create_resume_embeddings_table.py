"""create resume embeddings table

Revision ID: 778178c38ff4
Revises: 462695919f27
Create Date: 2026-03-24 00:38:12.174244

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = '778178c38ff4'
down_revision: Union[str, None] = '462695919f27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "resume_embeddings",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("resume_id", UUID(as_uuid=True), sa.ForeignKey("resumes.id"), nullable=False),
        sa.Column("embedding", Vector(384), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("resume_embeddings")
