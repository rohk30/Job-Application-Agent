'''
 The base SQL Query is as follows

ADD CONSTRAINT unique_application_per_candidate_job
UNIQUE (candidate_profile_id, job_posting_id);

CREATE TABLE applications (
    id UUID PRIMARY KEY,
    candidate_profile_id UUID NOT NULL REFERENCES candidate_profiles(id) ON DELETE CASCADE,
    job_posting_id UUID NOT NULL REFERENCES job_postings(id) ON DELETE CASCADE,
    resume_id UUID REFERENCES resumes(id),
    status TEXT NOT NULL CHECK (
        status IN (
            'discovered',
            'matched',
            'ready_to_apply',
            'applied',
            'assessment',
            'interview',
            'offer',
            'rejected',
            'ghosted'
        )
    ),
    match_score INTEGER CHECK (match_score BETWEEN 0 AND 100),
    applied_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (candidate_profile_id, job_posting_id)
);

CREATE INDEX idx_applications_candidate_profile_id ON applications(candidate_profile_id);
CREATE INDEX idx_applications_job_posting_id ON applications(job_posting_id);
CREATE INDEX idx_applications_status ON applications(status);

 '''

import uuid
from datetime import datetime
from sqlalchemy import (
    String,
    DateTime,
    Integer,
    ForeignKey,
    UniqueConstraint,
    CheckConstraint,
    Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base


class Application(Base):
    __tablename__ = "applications"

    __table_args__ = (
        UniqueConstraint(
            "candidate_profile_id",
            "job_posting_id",
            name="uq_applications_candidate_job"
        ),
        Index("idx_applications_candidate_profile_id", "candidate_profile_id"),
        Index("idx_applications_job_posting_id", "job_posting_id"),
        Index("idx_applications_status", "status"),
        CheckConstraint(
            """
            status IN (
                'discovered',
                'matched',
                'ready_to_apply',
                'applied',
                'assessment',
                'interview',
                'offer',
                'rejected',
                'ghosted'
            )
            """
        ),
        CheckConstraint("match_score BETWEEN 0 AND 100"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    candidate_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("candidate_profiles.id", ondelete="CASCADE"),
        nullable=False
    )

    job_posting_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("job_postings.id", ondelete="CASCADE"),
        nullable=False
    )

    resume_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("resumes.id")
    )

    status: Mapped[str] = mapped_column(String, nullable=False)

    match_score: Mapped[int | None] = mapped_column(Integer)

    applied_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    candidate_profile = relationship(
        "CandidateProfile",
        back_populates="applications"
    )

    job_posting = relationship(
        "JobPosting",
        back_populates="applications"
    )

    events = relationship("ApplicationEvent", back_populates="application")