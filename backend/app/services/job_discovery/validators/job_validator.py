from services.job_discovery.dto.parsed_job_data import ParsedJobData
from services.job_discovery.dto.validation_result import ValidationResult


class JobValidator:

    CLOSED_INDICATORS = [
        "position closed",
        "job expired",
        "no longer accepting applications",
        "job is no longer available",
    ]

    def validate(
        self,
        parsed_job: ParsedJobData
    ) -> ValidationResult:

        reasons = []

        # Mandatory fields
        if not parsed_job.company_name:
            reasons.append("Missing company name")

        if not parsed_job.title:
            reasons.append("Missing job title")

        if not parsed_job.job_description:
            reasons.append("Missing job description")

        if not parsed_job.raw_url:
            reasons.append("Missing raw URL")

        description_lower = parsed_job.job_description.lower()

        for indicator in self.CLOSED_INDICATORS:
            if indicator in description_lower:
                reasons.append(
                    f"Closed indicator detected: '{indicator}'"
                )
                break

        return ValidationResult(
            is_valid=(len(reasons) == 0),
            reasons=reasons
        )