'''
 The base SQL Query is as follows

CREATE TABLE job_sources (
    id UUID PRIMARY KEY,
    name TEXT UNIQUE NOT NULL, -- "Workday"
    trust_score NUMERIC(3,2) CHECK (trust_score BETWEEN 0 AND 1),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

 '''


import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Numeric, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base


class JobSource(Base):
    __tablename__ = "job_sources"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    trust_score: Mapped[float | None] = mapped_column(
        Numeric(3, 2),
        CheckConstraint("trust_score BETWEEN 0 AND 1")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    job_postings = relationship("JobPosting", back_populates="source")