# models/skill.py
import uuid
from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from db.base import Base

class Skill(Base):
    __tablename__ = "skills"

    __table_args__ = (
        UniqueConstraint("resume_id", "skill_name", name="uq_skill_resume"),
    )

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    resume_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("resumes.id", ondelete="CASCADE")
    )

    skill_name = mapped_column(String, index=True)

    resume = relationship("Resume", back_populates="skills")