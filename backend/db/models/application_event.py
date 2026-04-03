'''
 The base SQL Query is as follows

CREATE TABLE application_events (
    id UUID PRIMARY KEY,
    application_id UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
    previous_status TEXT,
    new_status TEXT NOT NULL,
    event_source TEXT NOT NULL, -- e.g., "agent", "user", "email_monitor"
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_application_events_application_id ON application_events(application_id);
CREATE INDEX idx_application_events_created_at ON application_events(created_at);

 '''

import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from db.base import Base


class ApplicationEvent(Base):
    __tablename__ = "application_events"

    __table_args__ = (
        Index("idx_application_events_application_id", "application_id"),
        Index("idx_application_events_created_at", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False
    )

    previous_status: Mapped[str | None] = mapped_column(String)

    new_status: Mapped[str] = mapped_column(String, nullable=False)

    event_source: Mapped[str] = mapped_column(String, nullable=False)

    event_metadata: Mapped[dict | None] = mapped_column("metadata", JSONB)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    application = relationship("Application", back_populates="events")