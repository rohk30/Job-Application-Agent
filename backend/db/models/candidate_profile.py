'''
 The base SQL Query is as follows

CREATE TABLE candidate_profiles (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT, -- e.g., "ML Engineer Profile"
    location_preferences TEXT[],
    role_preferences TEXT[],
    experience_level TEXT CHECK (experience_level IN ('intern', 'junior', 'mid', 'senior')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_candidate_profiles_user_id ON candidate_profiles(user_id);

 '''

import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    title: Mapped[str | None] = mapped_column(String)

    location_preferences: Mapped[list[str] | None] = mapped_column(
        ARRAY(String)
    )

    role_preferences: Mapped[list[str] | None] = mapped_column(
        ARRAY(String)
    )

    experience_level: Mapped[str | None] = mapped_column(
        String,
        CheckConstraint(
            "experience_level IN ('intern','junior','mid','senior')"
        )
    )

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

    resumes = relationship("Resume", back_populates="candidate_profile")
    applications = relationship("Application", back_populates="candidate_profile")