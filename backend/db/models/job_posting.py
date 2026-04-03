'''
 The base SQL Query is as follows

CREATE TABLE job_postings (
    id UUID PRIMARY KEY,
    source_id UUID NOT NULL REFERENCES job_sources(id),
    raw_url TEXT UNIQUE NOT NULL,
    company_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    location TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    discovered_at TIMESTAMPTZ NOT NULL,
    last_checked_at TIMESTAMPTZ,
    last_http_status INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_job_postings_source_id ON job_postings(source_id);
CREATE INDEX idx_job_postings_is_active ON job_postings(is_active);
CREATE INDEX idx_job_postings_company_title ON job_postings(company_name, job_title);

 '''


import uuid
from datetime import datetime
from sqlalchemy import (
    String,
    DateTime,
    Boolean,
    Integer,
    ForeignKey,
    Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base


class JobPosting(Base):
    __tablename__ = "job_postings"

    __table_args__ = (
        Index("idx_job_postings_source_id", "source_id"),
        Index("idx_job_postings_is_active", "is_active"),
        Index("idx_job_postings_company_title", "company_name", "job_title"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("job_sources.id"),
        nullable=False
    )

    raw_url: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    company_name: Mapped[str] = mapped_column(String, nullable=False)

    job_title: Mapped[str] = mapped_column(String, nullable=False)

    location: Mapped[str | None] = mapped_column(String)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    last_http_status: Mapped[int | None] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    source = relationship("JobSource", back_populates="job_postings")

    applications = relationship("Application", back_populates="job_posting")