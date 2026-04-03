from pydantic import BaseModel
from typing import List, Optional

class Experience(BaseModel):
    company: str
    role: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: str

class Education(BaseModel):
    institution: str
    degree: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class Project(BaseModel):
    name: str
    description: Optional[str] = None

class ResumeSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str]
    experience: List[Experience]
    education: List[Education]
    projects: List[Project] = []
    summary: Optional[str] = None
    raw_text: str