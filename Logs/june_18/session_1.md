# Session Log — June 18 | Session 1

## Overview
Catch-up log covering all work since the last logged session (April 7). Two main threads: (1) ingestion and search improvements committed on June 14, and (2) a major architectural decision to move away from CrewAI in favour of LangGraph + PydanticAI, committed June 19.

---

## What Was Done

### Ingestion — `embeddings_store.py`
- Added upsert logic: if an embedding already exists for a `resume_id`, update it in place instead of inserting a new row
- Note: this is intentional only for the embedding vector itself — full resume history (structured data) is still preserved

### Ingestion — `structured_store.py`
- Added delete-before-insert on re-upload: wipes existing `Skill`, `Experience`, `Education` rows for the resume before re-inserting
- Ensures re-uploads reflect the latest parsed version without accumulating stale rows

### New — `search_service.py`
- Implements `search_resumes(query, top_k)`: embeds a query string, runs cosine similarity search against `resume_embeddings` via pgvector (`<=>` operator), joins to `resumes`, `candidate_profiles`, `users`
- Returns ranked list of `{resume_id, name, email, score}` sorted by descending similarity score (`1 - distance`)
- Groundwork for the Strategy Matcher — not yet integrated into a route

### New — `Samples/sample_test/test_resumes.ipynb`
- Notebook for manually testing the resume pipeline end-to-end outside of FastAPI
- Added alongside existing `test_pipeline.py`

### Git housekeeping (June 14)
- `*.pdf` added to `.gitignore` — resume PDFs excluded from all future commits
- `docs/Job_Application_CoPilot.docx` committed — high-level product roadmap doc

### Docs restructure (June 14)
- `docs/architecture.md` moved to `docs/architectural_notes/architecture.md`
- `docs/architectural_notes/job_discovery.md` added — full breakdown of discovery pipeline philosophy, DTO design, provider strategy, no-LLM rationale

---

## Research Done

Before the architectural decision below was made, the following was researched and evaluated:

- **CrewAI** — original framework choice; good DX and prototyping speed but weak on persistence, long-lived state, and human-in-the-loop flows
- **LangGraph** — evaluated as a workflow orchestration layer; strong support for stateful graphs, interruptions, human approval nodes, retries, and persistent execution
- **PydanticAI** — evaluated as a structured reasoning layer; stateless, structured outputs via Pydantic models, cleaner than raw LLM calls for tasks like matching and resume editing
- **Temporal** — noted as a future option if workflows become month-long or distributed execution is needed; deferred for now
- Key insight: ApplyMate is a **stateful workflow orchestration problem**, not an autonomous multi-agent collaboration problem — the application lifecycle spans weeks/months and requires persistence, interruptibility, and HIL checkpoints that agent frameworks don't handle well

---

## Key Decision — ADR-001: Move Away From CrewAI

### File added: `docs/architectural_notes/adr_moveAwayFromCrewAI.md`

Previous assumption: CrewAI agents as the core orchestration layer.

New direction: **LangGraph** as the workflow engine + **PydanticAI** as the reasoning layer.

Updated stack:
| Layer       | Technology               |
|-------------|--------------------------|
| API         | FastAPI                  |
| Workflow    | LangGraph                |
| Reasoning   | PydanticAI               |
| ORM         | SQLAlchemy + Alembic     |
| DB          | PostgreSQL + pgvector    |

Architecture now follows:
```
FastAPI
↓
Application Services
↓
Repositories
↓
LangGraph Workflow Engine
↓
PydanticAI Reasoning Nodes
↓
LLMs
↓
PostgreSQL + pgvector
```

Frameworks are infrastructure — the domain model remains the center. This is consistent with the existing `Deterministic > AI > Human` principle.

### What stays deterministic
- Job discovery
- State transitions
- Event logging
- Application tracking

### What uses LLM
- Match scoring
- Resume editing
- Cover letter generation
- Interview preparation

### Evolution plan
- Phase 1 (current): build services, repos, use cases — framework-independent
- Phase 2: introduce LangGraph, convert use cases into workflow nodes
- Phase 3: wire full `Discover → Match → Edit → Apply → Track` graph
- Phase 4: human approval nodes, email monitoring, interview prep
- Phase 5: multi-user, background execution, long-lived sessions

---

## Files Touched
- `backend/app/ingestion/embeddings_store.py` — upsert logic added
- `backend/app/ingestion/structured_store.py` — delete-before-insert on re-upload
- `backend/app/services/search_service.py` — new; cosine similarity resume search
- `Samples/sample_test/test_resumes.ipynb` — new; manual pipeline test notebook
- `.gitignore` — `*.pdf` added
- `docs/Job_Application_CoPilot.docx` — added to repo
- `docs/architectural_notes/adr_moveAwayFromCrewAI.md` — new; ADR-001 formally documenting the CrewAI → LangGraph + PydanticAI decision

---

## Deferred / Known Issues
- 🟡 `search_service.py` not yet wired to a FastAPI route
- 🟡 DB credentials still hardcoded in `session.py` — no `.env` yet
- 🟡 Exception stubs in `job_discovery/exceptions/` still empty
- 🟡 `BaseSearchProvider`, `WorkdaySearchProvider`, `ProviderRegistry`, `DiscoveryService` all still stubs

---

## Next Steps
1. Implement `BaseSearchProvider` abstract interface
2. Implement `WorkdaySearchProvider` — Workday JSON endpoint fetching + pagination
3. Implement `ProviderRegistry` and `DiscoveryService`
4. Fill in exception classes
5. Wire `search_service.py` into a route once matching logic matures
