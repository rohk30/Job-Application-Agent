# pipeline.py

from .extractor import extract_text_from_pdf
from .cleaner import clean_text
from .segmenter import segment_sections
from .parser import (
    extract_email, extract_phone, extract_skills, extract_name,
    extract_summary, extract_experience, extract_education, extract_projects
)
from .embeddings import get_embedding
from .schema import ResumeSchema

def process_resume(file_path: str):
    raw_text = extract_text_from_pdf(file_path)
    cleaned = clean_text(raw_text)
    sections = segment_sections(cleaned)

    email = extract_email(cleaned)
    phone = extract_phone(cleaned)
    skills = extract_skills(cleaned)
    name = extract_name(sections)
    summary = extract_summary(sections)
    experience = extract_experience(sections)
    education = extract_education(sections)

    projects = extract_projects(sections)

    embedding = get_embedding(cleaned)

    return ResumeSchema(
        name=name,
        email=email,
        phone=phone,
        skills=skills,
        summary=summary,
        experience=experience,
        education=education,
        projects=projects,
        raw_text=cleaned
    ), embedding