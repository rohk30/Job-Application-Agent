from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from db.base import Base
import uuid


class ResumeEmbedding(Base):
    __tablename__ = "resume_embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"))
    embedding = Column(Vector(384))
