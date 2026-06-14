# structured_store.py

from backend.db.models import Skill, Experience, Education
from backend.db.session import SessionLocal


def store_structured_data(resume_id, data):
    db = SessionLocal()

    # Remove any existing structured records for this resume so re-uploads replace previous values
    db.query(Skill).filter_by(resume_id=resume_id).delete(synchronize_session=False)
    db.query(Experience).filter_by(resume_id=resume_id).delete(synchronize_session=False)
    db.query(Education).filter_by(resume_id=resume_id).delete(synchronize_session=False)

    # Skills
    for skill in data.skills:
        db.add(Skill(resume_id=resume_id, skill_name=skill))

    # Experience
    for exp in data.experience:
        db.add(Experience(
            resume_id=resume_id,
            company=exp.company,
            role=exp.role,
            start_date=exp.start_date,
            end_date=exp.end_date,
            description=exp.description
        ))

    # Education
    for edu in data.education:
        db.add(Education(
            resume_id=resume_id,
            institution=edu.institution,
            degree=edu.degree,
            start_date=edu.start_date,
            end_date=edu.end_date
        ))

    db.commit()
    db.close()