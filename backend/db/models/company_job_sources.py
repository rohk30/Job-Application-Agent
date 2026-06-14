# db/models/company_job_sources.py

import uuid

from sqlalchemy import (
    Boolean,
    DateTime,
    String,
    Text,
    func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class CompanyJobSource(Base):
    __tablename__ = "company_job_sources"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    company_name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True
    )

    source_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="workday"
    )

    base_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True
    )

    enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    last_crawled_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )