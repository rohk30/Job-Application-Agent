# Job Discovery Architecture Notes

## Philosophy

The Job Discovery subsystem is intentionally designed as a deterministic pipeline. AI and CrewAI agents are deliberately excluded at this stage.

Principle:

```
Code > AI > Human
```

Use deterministic code whenever possible, AI only when uncertainty begins, and human intervention only at trust boundaries.

---

# Discovery Pipeline

```
WorkdaySearchProvider
        ↓
RawJobData
        ↓
JobPageParser
        ↓
ParsedJobData
        ↓
JobValidator
        ↓
ValidationResult
        ↓
DiscoveredJob
        ↓
DiscoveryService
        ↓
JobPostingRepository
        ↓
job_postings table
```

No CrewAI.

No LLM calls.

No candidate matching.

---

# DTO Layer

### RawJobData

Represents raw provider output.

Purpose:

* Provider-specific data contract.
* Closest representation of external response.

---

### ParsedJobData

Internal normalized representation.

Purpose:

* Provider-independent format.
* Input to validators.

---

### ValidationResult

Represents whether a job should enter the system.

Contains:

* is_valid
* reasons

---

### DiscoveredJob

Final object ready for persistence.

Purpose:

* Repository-facing DTO.
* Decouples persistence from parsing.

---

# Separation of Concerns

### Parser

Responsibilities:

* String cleanup
* Normalization
* DTO transformation

Parser should NOT:

* Perform validation
* Contain business logic
* Call LLMs
* Access databases

---

### Validator

Responsibilities:

* Mandatory field checks
* Closed job detection
* Quality gate before persistence

Validator should NOT:

* Parse data
* Call external APIs
* Access databases

---

### DiscoveryService

Acts as the orchestrator.

Responsibilities:

1. Fetch jobs from providers.
2. Parse jobs.
3. Validate jobs.
4. Persist valid jobs.

DiscoveryService owns workflow orchestration only.

---

# Why No LLMs Yet?

At this stage, jobs come from Workday JSON endpoints.

These responses are already structured.

Using LLMs here would introduce:

* Additional cost
* Increased latency
* Hallucination risks
* Non-determinism

Current philosophy:

```
Deterministic solutions first.
```

AI should only appear when deterministic approaches are insufficient.

---

# Provider Architecture

Current:

```
providers/
    workday/
```

Future:

```
providers/
    workday/
    greenhouse/
    lever/
    linkedin/
    company_websites/
```

Each provider should expose a common interface.

---

# Workday Data Acquisition Strategy

Primary strategy:

### Workday JSON endpoints

Advantages:

* Free
* Structured responses
* Faster
* Easier pagination
* More stable than HTML scraping

No API keys are required.

---

Secondary strategy:

### HTML fallback

Used only when JSON endpoints are unavailable.

---

Browser automation (Playwright) is NOT part of job discovery.

Playwright belongs to the Application Assistant subsystem.

---

# Parser Philosophy

Current:

```
RawJobData
↓
JobPageParser
↓
ParsedJobData
```

Future:

```
workday_parser.py
greenhouse_parser.py
lever_parser.py
company_website_parser.py
llm_normalizer.py
```

LLM normalization will only be introduced when supporting arbitrary websites and unstructured pages.

AI is considered an implementation detail, not an architectural dependency.

---

# Folder Structure

```
services/
    job_discovery/

        discovery_service.py

        providers/
            provider_registry.py

            workday/
                workday_search_provider.py

        parsers/
            job_page_parser.py

        validators/
            job_validator.py

        dto/
            raw_job_data.py
            parsed_job_data.py
            validation_result.py
            discovered_job.py

        exceptions/
            discovery_exception.py
            parsing_exception.py
            validation_exception.py
```

---

# Coding Order

1. DTOs
2. JobValidator
3. JobPageParser
4. BaseSearchProvider
5. WorkdaySearchProvider
6. ProviderRegistry
7. DiscoveryService

---

# Future CrewAI Integration

CrewAI agents should wrap mature services.

Eventually:

```python
@tool
def discover_jobs():
    return discovery_service.discover_jobs()
```

The Headhunter Agent should remain thin and focus on reasoning, not implementation.

---

# Guiding Principle

Build deterministic, testable services first.

Introduce agents only after the underlying subsystem is mature and independently reliable.
