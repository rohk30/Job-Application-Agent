import uuid
from fastapi import APIRouter, UploadFile, File, Form
from backend.app.services.resume_service import handle_resume_upload

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(
    candidate_profile_id: uuid.UUID = Form(...),
    file: UploadFile = File(...)
):
    result = handle_resume_upload(file, candidate_profile_id=candidate_profile_id)
    return result
