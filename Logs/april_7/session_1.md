# Session Log — April 7 | Session 1

## Overview
This session focused on two things: project housekeeping (git setup, gitignore, session log conventions) and laying the structural foundation for the Job Discovery subsystem — DTOs, exceptions, parser, validator, domain enums, and the overall folder architecture. No provider or service logic was implemented yet.

---

## Environment / Setup Changes
None.

---

## Files Created

### Git & Logs
- `.gitignore` — updated to exclude `*.pdf` across the entire repo (privacy — resume PDFs should never be committed)
- `Logs/SESSION_LOG_GUIDELINES.md` — conventions for writing session logs; covers long session format, short session format, general rules, and project-specific reminders

### Docs
- `docs/architectural_notes/` — new subdirectory created to house all subsystem-level architecture notes
- `docs/architectural_notes/architecture.md` — moved from `docs/architecture.md`; content unchanged
- `docs/architectural_notes/job_discovery.md` — new; full architecture breakdown for the job discovery subsystem (pipeline, DTO layer, separation of concerns, provider strategy, coding order, future CrewAI integration)

### Domain Enums
- `backend/app/domain/enums/employment_type.py` — `EmploymentType` StrEnum: `FULL_TIME`, `INTERN`, `CONTRACT`
- `backend/app/domain/enums/experience_level.py` — `ExperienceLevel` StrEnum: `ENTRY`, `MID`, `SENIOR`
- `backend/app/domain/enums/source_type.py` — `SourceType` StrEnum: `WORKDAY`, `GREENHOUSE`, `LEVER`

### Job Discovery — DTOs
- `backend/app/services/job_discovery/dto/raw_job_data.py` — `RawJobData`: provider-specific output, closest to external response
- `backend/app/services/job_discovery/dto/parsed_job_data.py` — `ParsedJobData`: normalized, provider-independent; input to validator
- `backend/app/services/job_discovery/dto/validation_result.py` — `ValidationResult`: `is_valid` + `reasons` list
- `backend/app/services/job_discovery/dto/discovered_job.py` — `DiscoveredJob`: final repository-facing DTO

### Job Discovery — Exceptions
- `backend/app/services/job_discovery/exceptions/discovery_exception.py` — stub
- `backend/app/services/job_discovery/exceptions/parsing_exception.py` — stub
- `backend/app/services/job_discovery/exceptions/validation_exception.py` — stub

### Job Discovery — Core Logic
- `backend/app/services/job_discovery/parsers/job_page_parser.py` — `JobPageParser`: strips and normalizes `RawJobData` → `ParsedJobData`; no business logic, no LLM calls
- `backend/app/services/job_discovery/validators/job_validator.py` — `JobValidator`: mandatory field checks + closed job detection via `CLOSED_INDICATORS` list; returns `ValidationResult`

### Job Discovery — Stubs (to be implemented)
- `backend/app/services/job_discovery/providers/base_provider.py` — stub
- `backend/app/services/job_discovery/providers/workday_search_provider.py` — stub
- `backend/app/services/job_discovery/providers/providers_registry.py` — stub
- `backend/app/services/job_discovery/discovery_service.py` — stub

---

## Files Modified

- `backend/db/models/__init__.py` — added `CompanyJobSource` import and added it to `__all__`
- `backend/app/ingestion/embeddings_store.py` — modified (details in prior session)
- `backend/app/ingestion/structured_store.py` — modified (details in prior session)
- `docs/` — reorganized; `architecture.md` moved into `docs/architectural_notes/`

---

## Database Changes
- Migration `3fffb7cd05ee_add_company_job_sources_table.py` — generated and applied
- Adds `company_job_sources` table with: `id` (UUID PK), `company_name` (unique), `source_type`, `base_url` (unique), `enabled`, `last_crawled_at`, `created_at`, `updated_at`
- Verified with `alembic current` → confirmed at `head`

---

## Decisions Made

### Deterministic > AI > Human
Core engineering principle formally established this session. Applied directly to the Job Discovery subsystem:
- No CrewAI, no LLM calls in the discovery pipeline
- Workday returns structured JSON — deterministic parsing is sufficient and preferred
- LLM normalization deferred to when arbitrary/unstructured HTML sources are added (e.g. company websites)

### DTO Pipeline Design
Explicit DTO boundaries enforced at each stage:
```
RawJobData → ParsedJobData → ValidationResult → DiscoveredJob
```
Each DTO has a single owner — parser, validator, or service. No object bleeds across layers.

### Parser Responsibility
Parser does string cleanup and normalization only. No validation, no business logic, no external calls.

### Validator Responsibility
Validator enforces mandatory fields and closed job detection only. No parsing, no DB access, no external calls.

### Closed Job Detection
Deterministic string matching against `CLOSED_INDICATORS` list — not LLM-based. Fast, free, predictable.

### Playwright excluded from Job Discovery
Browser automation belongs to the Application Assistant subsystem. Discovery uses Workday JSON endpoints directly.

### Resume history intentionally kept
No deduplication on `resume_embeddings`, `experience`, or `education` rows. A candidate may update their resume regularly and full history is a feature, not a bug.

---

## Current Job Discovery State

| Component             | Status        |
|-----------------------|---------------|
| DTOs (all 4)          | ✅ Done       |
| Domain enums          | ✅ Done       |
| Exceptions            | ✅ Stubs only |
| JobPageParser         | ✅ Done       |
| JobValidator          | ✅ Done       |
| BaseSearchProvider    | ⏳ Stub       |
| WorkdaySearchProvider | ⏳ Stub       |
| ProviderRegistry      | ⏳ Stub       |
| DiscoveryService      | ⏳ Stub       |

---

## Deferred / Known Issues

- 🟡 `.env` for DB credentials — `session.py` still has hardcoded DB URL in plaintext
- 🟡 Exception classes are stubs — need actual definitions before error handling can be wired in
- 🟡 `WorkdaySearchProvider` not implemented — next major build item
- 🟢 `search_service.py` added but not yet integrated — will feed into Strategy Matcher later

---

## Run Commands
```
# From: c:\My_Programs\Job Application Agent\backend
set PYTHONPATH=c:\My_Programs\Job Application Agent\backend
uv run alembic revision --autogenerate -m "add_company_job_sources_table"
uv run alembic upgrade head
```
Docker container must be running before any alembic command.

---

## Next Steps
1. Implement `BaseSearchProvider` abstract interface
2. Implement `WorkdaySearchProvider` — Workday JSON endpoint fetching + pagination
3. Implement `ProviderRegistry`
4. Implement `DiscoveryService` — orchestrates fetch → parse → validate → persist
5. Fill in exception classes
