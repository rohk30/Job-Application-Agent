"""add ivfflat index on resume embeddings

Revision ID: 3c2bb7270b17
Revises: 778178c38ff4
Create Date: 2026-03-24 00:47:49.526855

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c2bb7270b17'
down_revision: Union[str, None] = '778178c38ff4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE INDEX resume_embedding_idx
        ON resume_embeddings
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100);
    """)


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS resume_embedding_idx;")
