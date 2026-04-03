from fastapi import FastAPI
from app.routes.resume import router as resume_router

app = FastAPI(title="Job Application Agent")

app.include_router(resume_router, prefix="/api/v1")