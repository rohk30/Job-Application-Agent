from pydantic import BaseModel


class DiscoveredJob(BaseModel):
    title: str
    company_name: str
    raw_url: str
    job_description: str
    location: str | None
    employment_type: str | None
    experience_level: str | None