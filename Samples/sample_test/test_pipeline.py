import uuid
from backend.app.services.resume_service import handle_resume_upload
from backend.db.session import SessionLocal
from backend.db.models import User, CandidateProfile



def seed_test_candidate():
    db = SessionLocal()
    user = db.query(User).filter_by(email="test@test.com").first()
    if not user:
        user = User(email="test@test.com", full_name="Test User")
        db.add(user)
        db.commit()
        db.refresh(user)
    profile = db.query(CandidateProfile).filter_by(user_id=user.id).first()
    if not profile:
        profile = CandidateProfile(user_id=user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    db.close()
    return profile.id

resume_path = r"..\sample_test_data\RohitDataResume.pdf"
candidate_profile_id = seed_test_candidate()

with open(resume_path, "rb") as f:
    result = handle_resume_upload(f, candidate_profile_id=candidate_profile_id)

print("=== Extracted Details ===")
print(f"Resume ID  : {result['resume_id']}")
parsed = result["parsed_data"]
print(f"Name       : {parsed['name']}")
print(f"Email      : {parsed['email']}")
print(f"Phone      : {parsed['phone']}")
print(f"Skills     : {parsed['skills']}")
print(f"Experience : {parsed['experience']}")
print(f"Education  : {parsed['education']}")
print(f"Projects   : {parsed['projects']}")

print("\n=== Raw Text ===")
print(parsed["raw_text"])
