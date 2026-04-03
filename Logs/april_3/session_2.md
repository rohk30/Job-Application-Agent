# Session Log — April 3 | Session 2

## Overview
This session focused on wiring up the FastAPI endpoint end-to-end, verifying that parsed structured resume data is correctly persisted to the database, and fixing all issues encountered along the way.

---

## Modifications Made

### 1. `resume_service.py` — Full Pipeline Orchestration
- Reordered steps: file save → process resume → create DB entry → store embedding → store structured data
- `process_resume()` now runs before `create_resume_entry()` so parsed fields (name, email, phone, summary, raw_text) can be passed directly into the resume row
- Added `store_structured_data()` call (step 5) which was previously a commented-out placeholder

### 2. `intake.py` — Stores Parsed Fields on Resume Row
- `create_resume_entry()` now accepts `raw_text`, `name`, `email`, `phone`, `summary`
- On re-upload: updates existing resume row with new parsed values instead of just returning the existing id
- Fixed `raw_text` being hardcoded as `""` — now stores actual extracted text

### 3. `structured_store.py` — New File
- Stores skills, experience, and education into their respective tables
- Called as the final step in `resume_service.py`

### 4. `resume.py` (model) — New Columns
- Added `name`, `email`, `phone`, `summary` as nullable columns
- Changed `raw_text` column type from `VARCHAR` to `Text`
- Added relationships to `Skill`, `Experience`, `Education`

### 5. `skill.py` (model) — Unique Constraint Added
- Added `UniqueConstraint("resume_id", "skill_name", name="uq_skill_resume")` to prevent duplicate skills per resume

### 6. `session.py` — Fixed DB URL
- Default `DATABASE_URL` was pointing to the `postgres` database instead of `mydb`
- Fixed to `postgresql+psycopg://postgres:12345678@localhost:5433/mydb`

### 7. `alembic.ini` — Fixed DB URL
- Same issue as `session.py` — was pointing to `postgres` database
- Fixed to `mydb`

---

## Challenges Faced

### Uvicorn Import Error — Wrong Module Name
- `resume_service.py` had `from backend.app.ingestion.data_store import store_structured_data`
- The actual file is named `structured_store.py` — caused `ModuleNotFoundError` on startup

### First POST Request Hung Indefinitely
- Root cause: `SentenceTransformer("all-MiniLM-L6-v2")` downloads ~90MB model on first import at module load time
- No error, no timeout — just silently hung
- Fix: pre-downloaded the model by running it once directly in the terminal

### Migrations Applied to Wrong Database
- `alembic.ini` and `session.py` both had `postgres` as the DB name instead of `mydb`
- Alembic reported being at `head` but `\dt` in `mydb` showed no tables at all
- Fix: corrected both URLs to `mydb`, stamped base, and re-ran `alembic upgrade head`

### FK Violation on First POST to Correct DB
- `candidate_profile_id` used in the request didn't exist in the freshly migrated `candidate_profiles` table
- Fix: manually inserted a test user and candidate profile with the matching UUID

### Unique Constraint Migration Blocked by Existing Duplicates
- Previous test runs (before the fix) had inserted duplicate skills
- `alembic upgrade head` failed with `UniqueViolation` when trying to create `uq_skill_resume`
- Fix: deleted duplicate skill rows, cleared all test data, then re-ran the migration successfully

### Experience Description Stored Character-by-Character
- `structured_store.py` had `"\n".join(exp.description)` — since `description` is a `str` (not a list), this iterated over individual characters
- Fix: changed to `exp.description` directly

---

## Issues Fixed

| Issue | Fix |
|-------|-----|
| `raw_text` stored as empty string | Pass `parsed_data.raw_text` into `create_resume_entry()` |
| Parsed fields (name, email, etc.) not saved to `resumes` table | Added columns to model + migration, passed values from service |
| Structured data (skills, experience, education) never stored | Implemented `structured_store.py` and wired it into service |
| Wrong DB URL in `alembic.ini` and `session.py` | Changed `postgres` → `mydb` in both |
| Duplicate skills inserted on re-upload | Added `UniqueConstraint` on `(resume_id, skill_name)` |
| Experience description garbled | Fixed `"\n".join(str)` → use `str` directly |

---

## Verification (SQL Queries Run Post-Fix)

All fields confirmed correct after a clean POST request:

- `resumes` — name, email, phone, summary all populated correctly
- `skills` — 16 unique skills, no duplicates
- `experience` — 1 entry with full readable description (Talent Recruit, ML Intern, 05/2024–07/2024)
- `education` — 3 entries (VIT Vellore, Geetanjali Olympiad School, New Horizon Public School)

---

## Next Steps

- Move DB credentials out of hardcoded defaults in `session.py` into a `.env` file
- Handle duplicate experience/education rows on re-upload (similar to how skills are now deduplicated)
- Add deduplication for `resume_embeddings` — currently inserts a new row on every upload
- Expand `KNOWN_SKILLS` or replace with NER/taxonomy-based skill extraction
- Add proper error handling and HTTP error responses in the route layer
