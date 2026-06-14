from pydantic import BaseModel


class ParsedJobData(BaseModel):
    title: str
    company_name: str
    raw_url: str
    job_description: str
    external_job_id: str
    location: str | None = None
    employment_type: str | None = None
    experience_level: str | None = None