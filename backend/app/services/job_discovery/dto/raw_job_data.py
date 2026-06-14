from pydantic import BaseModel


class RawJobData(BaseModel):
    external_job_id: str
    title: str
    company_name: str
    raw_url: str
    job_description: str
    location: str | None = None
    employment_type: str | None = None
    experience_level: str | None = None