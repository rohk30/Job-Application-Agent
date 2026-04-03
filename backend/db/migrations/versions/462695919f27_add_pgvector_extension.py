"""add pgvector extension

Revision ID: 462695919f27
Revises: 8e8a8e2c71fd
Create Date: 2026-03-24 00:37:34.346915

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '462695919f27'
down_revision: Union[str, None] = '8e8a8e2c71fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS vector;")
