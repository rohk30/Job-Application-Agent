from services.job_discovery.dto.raw_job_data import RawJobData
from services.job_discovery.dto.parsed_job_data import ParsedJobData


class JobPageParser:

    def parse(
        self,
        raw_job: RawJobData
    ) -> ParsedJobData:

        return ParsedJobData(
            external_job_id=raw_job.external_job_id.strip(),

            title=raw_job.title.strip(),

            company_name=raw_job.company_name.strip(),

            raw_url=raw_job.raw_url.strip(),

            job_description=raw_job.job_description.strip(),

            location=(
                raw_job.location.strip()
                if raw_job.location
                else None
            ),

            employment_type=(
                raw_job.employment_type.strip()
                if raw_job.employment_type
                else None
            ),

            experience_level=(
                raw_job.experience_level.strip()
                if raw_job.experience_level
                else None
            )
        )