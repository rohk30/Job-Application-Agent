# models/education.py
import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base

class Education(Base):
    __tablename__ = "education"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    resume_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("resumes.id", ondelete="CASCADE")
    )

    institution = mapped_column(String)
    degree = mapped_column(String)
    start_date = mapped_column(String)
    end_date = mapped_column(String)

    resume = relationship("Resume", back_populates="education")