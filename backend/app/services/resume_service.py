# app/services/resume_service.py

from backend.app.ingestion.storage import save_file_locally
from backend.app.ingestion.pipeline import process_resume
from backend.app.ingestion.embeddings_store import store_embedding
from backend.app.ingestion.intake import create_resume_entry
from backend.app.ingestion.structured_store import store_structured_data
# 

def handle_resume_upload(file, candidate_profile_id):
    print("1. saving file...")
    file_path = save_file_locally(file, candidate_profile_id)

    print("2. processing resume...")
    parsed_data, embedding = process_resume(file_path)

    print("3. creating DB entry with parsed data...")
    resume_id = create_resume_entry(
        candidate_profile_id=candidate_profile_id,
        file_url=file_path,
        raw_text=parsed_data.raw_text,
        name=parsed_data.name,
        email=parsed_data.email,
        phone=parsed_data.phone,
        summary=parsed_data.summary
    )

    print("4. storing embedding...")
    store_embedding(resume_id, embedding)

    print("5. storing structured data...")
    store_structured_data(resume_id, parsed_data)

    print("6. done")

    return {
        "resume_id": resume_id,
        "parsed_data": parsed_data.dict()
    }