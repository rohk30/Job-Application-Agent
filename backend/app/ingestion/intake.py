# ingestion/intake.py

from backend.db.session import SessionLocal
from backend.db.models.resume import Resume
from datetime import datetime, timezone
import uuid


def create_resume_entry(
    candidate_profile_id: uuid.UUID,
    file_url: str,
    raw_text: str,
    name: str | None,
    email: str | None,
    phone: str | None,
    summary: str | None
):
    db = SessionLocal()

    existing = db.query(Resume).filter_by(
        candidate_profile_id=candidate_profile_id,
        version_label="base"
    ).first()

    if existing:
        # update existing instead of returning
        existing.raw_text = raw_text
        existing.name = name
        existing.email = email
        existing.phone = phone
        existing.summary = summary

        db.commit()
        db.refresh(existing)

        db.close()
        return existing.id

    resume = Resume(
        candidate_profile_id=candidate_profile_id,
        version_label="base",
        raw_text=raw_text,          # ✅ FIXED
        file_url=file_url,
        name=name,
        email=email,
        phone=phone,
        summary=summary,
        created_at=datetime.now(timezone.utc)
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)
    db.close()

    return resume.id