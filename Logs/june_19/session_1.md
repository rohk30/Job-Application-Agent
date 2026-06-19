# Session Log — June 19 | Session 1

## What Was Done
- Manually inspected network responses of Workday career sites across 5 companies: NVIDIA, Salesforce, Adobe, Samsung, Qualcomm
- Documented response schemas, common fields, edge cases, and company-specific observations
- Drafted a reverse engineering plan tracking the evolution of the provider architecture decision
- Identified key edge cases that affect parser and DTO design

## Why
To determine whether a single `WorkdaySearchProvider` can handle all Workday tenants or whether company-specific providers are needed.

## Key Findings

### Workday protocol is standardized across tenants
- Tested tenants: `wd3`, `wd5`, `wd12`
- Search endpoint: `POST /wday/cxs/<tenant>/<site>/jobs` — identical schema across all companies
- Detail endpoint: returns `jobPostingInfo`, `hiringOrganization`, `similarJobs`, `userAuthenticated` — identical across all companies
- Tenant subdomain (wd3/wd5/wd12) does not affect payload structure
- Conclusion: one `WorkdaySearchProvider` handles all companies — no company-specific providers needed

### Job description section names are unstable
- NVIDIA: `What you'll be doing`, `What we need to see`, `Ways to stand out`
- Samsung: `Position Summary`, `Skills and Qualifications`
- Qualcomm: `General Summary`, `Minimum Qualifications`, `Preferred Qualifications`, `Principal Duties and Responsibilities`
- Conclusion: deterministic section extraction is unreliable — LLM understanding is the right approach here

### Parser architecture updated
Previous plan:
```
RawJobData → JobPageParser → ParsedJobData
```
New plan:
```
RawJobData → HtmlCleaner → PlainJobDocument → LLMJobUnderstandingService → EnrichedJobData → JobValidator → Repository
```
Reason: semantic meaning (responsibilities, skills, YOE, keywords) is stable across companies; section names are not. LLM is the right tool here — this is one of the genuine `AI` cases in `Deterministic > AI > Human`.

### Notable company-specific observations
- Salesforce: exposes `endDate`, `timeLeftToApply`, `remoteType` — useful urgency and remote signals
- Adobe: `similarJobs` heavily populated — job graph expansion possible in future
- Samsung: search response exposes `facets` (country, job category, time type, locations) — filters can be discovered dynamically
- Qualcomm: confirms section name instability; also has large `similarJobs`

### Optional fields confirmed (must not be required in DTO)
`additionalLocations`, `remoteType`, `endDate`, `questionnaireId`, `timeLeftToApply`, `similarJobs`

### HTML quality warning
Job descriptions contain nested spans, div soup, inline styles, hyperlinks, malformed HTML — must be cleaned before any LLM processing.

## Files Touched
- `docs/research/My_Research/workday_response_schema.md` — search + detail endpoint schemas, `jobPostingInfo` fields
- `docs/research/My_Research/workday_common_fields.md` — mandatory vs optional fields, nested structures, DTO split recommendation
- `docs/research/My_Research/workday_companies_sample.md` — per-company observations (NVIDIA, Salesforce, Adobe, Samsung, Qualcomm)
- `docs/research/My_Research/workday_edge_cases.md` — section name variance, optional fields, HTML quality issues
- `docs/research/My_Research/workday_reverse_engineering_plan.md` — 7-phase journey from company-specific providers → single `WorkdaySearchProvider` + LLM understanding layer

## Next Steps
- Implement `WorkdaySearchProvider` using confirmed endpoint schema
- Implement `HtmlCleaner` to strip job description HTML before LLM processing
- Design `LLMJobUnderstandingService` to extract structured fields from plain job text
- Update `RawJobData` DTO to include optional fields (`remoteType`, `endDate`, `timeLeftToApply`)
