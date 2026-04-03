'''
 The base SQL Query is as follows

CREATE TABLE resumes (
    id UUID PRIMARY KEY,
    candidate_profile_id UUID NOT NULL REFERENCES candidate_profiles(id) ON DELETE CASCADE,
    version_label TEXT NOT NULL, -- e.g., "base", "ml_focused", "backend_focused"
    raw_text TEXT NOT NULL,
    file_url TEXT, -- S3/MinIO location
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (candidate_profile_id, version_label)
);

CREATE INDEX idx_resumes_candidate_profile_id ON resumes(candidate_profile_id);

 '''


import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, UniqueConstraint, Index, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base


class Resume(Base):
    __tablename__ = "resumes"

    __table_args__ = (
        UniqueConstraint(
            "candidate_profile_id",
            "version_label",
            name="uq_resume_profile_version"
        ),
        Index("idx_resumes_candidate_profile_id", "candidate_profile_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    candidate_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("candidate_profiles.id", ondelete="CASCADE"),
        nullable=False
    )

    version_label: Mapped[str] = mapped_column(String, nullable=False)

    name: Mapped[str | None] = mapped_column(String)
    email: Mapped[str | None] = mapped_column(String, index=True)
    phone: Mapped[str | None] = mapped_column(String)
    summary: Mapped[str | None] = mapped_column(String)

    raw_text: Mapped[str] = mapped_column(Text, nullable=False)

    file_url: Mapped[str | None] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    candidate_profile = relationship(
        "CandidateProfile",
        back_populates="resumes"
    )

    skills = relationship(
        "Skill",
        back_populates="resume",
        cascade="all, delete-orphan"
    )

    experiences = relationship(
        "Experience",
        back_populates="resume",
        cascade="all, delete-orphan"
    )

    education = relationship(
        "Education",
        back_populates="resume",
        cascade="all, delete-orphan"
    )