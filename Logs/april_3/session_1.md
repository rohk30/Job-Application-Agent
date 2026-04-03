# Session Log — April 3 | Session 1

## Overview
This session focused on setting up the resume ingestion pipeline end-to-end — from PDF extraction to embedding storage in PostgreSQL — and iteratively fixing issues until the full pipeline ran successfully.

---

## Environment Setup

### Packages Installed (via `uv add`)
`pdfplumber`, `pydantic`, `sentence-transformers`, `numpy`, `scikit-learn`, `spacy`, `rapidfuzz`, `sqlalchemy`, `psycopg2-binary`, `pgvector`, `en_core_web_sm` (spaCy model)

### Key Decision: `uv` over `pip`
The project uses `uv` for dependency management. `pip` is not available in the venv, so all installs go through `uv add` or direct wheel URLs (used for `en_core_web_sm`).

---

## Database Setup

### pgvector Extension
- **Original situation:** Using `postgres:16` Docker image which does not ship with the `vector` extension.
- **Fix:** Switched `docker-compose.yml` image to `pgvector/pgvector:pg16` which has the extension pre-installed.
- **Migration created:** `462695919f27_add_pgvector_extension.py` — runs `CREATE EXTENSION IF NOT EXISTS vector;`

### Resume Embeddings Table
- **Original situation:** `resume_embeddings` table defined with `Integer` for `id` and `resume_id`, but `resumes.id` is a `UUID`.
- **Fix:** Rewrote migration `778178c38ff4` and `ResumeEmbedding` model to use `UUID` columns with a proper FK to `resumes.id`.
- **Why:** PostgreSQL cannot cast UUID to Integer — caused a hard crash on insert.

### IVFFlat Index
- Migration `3c2bb7270b17` adds a cosine similarity index on the `embedding` column for fast ANN search.
- `lists = 100` chosen as a reasonable default for a small-to-medium dataset.

---

## Ingestion Pipeline

### Files Created
`backend/app/ingestion/`: `pipeline.py`, `extractor.py`, `cleaner.py`, `segmenter.py`, `parser.py`, `embeddings.py`, `schema.py`, `utils.py`, `embeddings_store.py`, `intake.py`

### Embedding Model
- Using `sentence-transformers/all-MiniLM-L6-v2` — 384-dimensional embeddings.
- Public model, no HuggingFace token required. The `UNEXPECTED` key warning on load (`embeddings.position_ids`) is safe to ignore.

---

## Issues Fixed This Session

### 1. Mixed Import Paths (SQLAlchemy Table Double-Registration)
- **Problem:** Some files used `db.*` imports, others used `backend.db.*`. With `PYTHONPATH` set to both project root and `backend/`, Python treated them as different modules and SQLAlchemy tried to register the same tables twice → `InvalidRequestError: Table 'users' is already defined`.
- **Fix:** Standardised all imports across `embeddings_store.py`, `intake.py`, `resume_service.py`, and `test_pipeline.py` to use the `backend.*` prefix consistently.
- **Thought process:** The root cause was two module resolution paths for the same physical file. Picking one canonical prefix and sticking to it eliminates the ambiguity.

### 2. `cleaner.py` Collapsing Newlines
- **Original:** `re.sub(r'\s+', ' ', text)` collapsed all whitespace including newlines into a single space → segmenter received one long line, found no section headers.
- **Fix:** Rewrote cleaner to process line-by-line, only collapsing spaces within a line, preserving `\n` between lines.
- **Impact:** Segmenter now correctly identifies sections.

### 3. Segmenter False-Positive Section Headers
- **Original:** Any line *containing* a section keyword (e.g. "experience in ML") was treated as a section header.
- **Fix:** Only lines that *are* the header (short, no trailing punctuation, exact match) trigger a new section.

### 4. `intake.py` Wrong Resume Model Fields
- **Original:** Used `user_id`, `file_path`, `version` — none of which exist on the `resumes` table.
- **Fix:** Updated to use `candidate_profile_id`, `file_url`, `version_label="base"` matching the actual schema.
- **Added upsert logic:** If a resume with the same `(candidate_profile_id, version_label)` already exists, return the existing `id` instead of inserting — avoids unique constraint violation on repeated test runs.

### 5. `storage.py` FastAPI vs Plain File Handle
- **Original:** `file.file.read()` assumed a FastAPI `UploadFile` object.
- **Fix:** `content = file.file.read() if hasattr(file, 'file') else file.read()` — handles both.

### 6. Pydantic v2 Optional Fields Without Defaults
- **Problem:** Pydantic v2 requires `Optional[str]` fields to have `= None` default, otherwise they're treated as required.
- **Fix:** Added `= None` to all `Optional` fields in `ResumeSchema`, `Experience`, and `Education`.

### 7. Parser — Education & Experience Empty
- **Root cause:** Cleaner was collapsing newlines (see #2). Once fixed, sections were populated.
- **Education parser:** Rewrote to use pipe-split (`|`) as primary strategy, NER as fallback. Now correctly extracts institution, degree, and dates.
- **Experience parser:** Same pipe-split + NER approach. Detects entry headers by presence of a date pattern on a short line.

### 8. Date Extraction Returning None
- **Problem:** `DATE_PATTERN.findall()` returns tuples from capture groups — `MM/YYYY` format matched a non-capturing branch so dates came back empty.
- **Fix:** Added a direct `re.findall(r'\d{2}/\s*\d{4}', line)` pass as the primary token extractor.

---

## Schema Changes
- Added `summary: Optional[str] = None` to `ResumeSchema`
- Added `Project` model: `name: str`, `description: Optional[str]`
- Added `projects: List[Project] = []` to `ResumeSchema`
- `Experience.description` changed from `List[str]` to `str`

---

## Current State of Extraction (on sample resume)

| Field       | Status |
|-------------|--------|
| Email       | ✅ Correct |
| Phone       | ✅ Correct |
| Skills      | ✅ 16 skills detected |
| Experience  | ✅ 1 entry (only 1 in resume) — company, role, dates, description all correct |
| Education   | ✅ 3 entries — institution, degree, dates all correct |
| Projects    | ✅ 2 named projects extracted |
| Name        | ✅ Correct |
| Summary     | ✅ Extracted |

---

## Deferred Issues / Future Work

### 🔴 Immediate & Urgent
- ~~**Name extraction not implemented**~~ — Fixed in this session. Uses first clean short line from the `general` section (no digits, emails, or special chars, max 5 words).

### 🟡 On-Need Basis (Can Be Revisited Later)
- **Nameless projects** — Projects without an explicit heading (e.g. `Designed a calculator app...`, `Developed a Tic-Tac-Toe game...`) currently get absorbed into the description of the last named project (`Customized Chatbot`). Decided to defer — need a smarter heuristic or LLM call to handle these cleanly without over-engineering.
- **Skills list is hardcoded** — `KNOWN_SKILLS` is a fixed set. Will miss domain-specific or niche skills. Should be replaced with a broader skills taxonomy or NER-based extraction.
- **Segmenter robustness** — Current section detection relies on exact header matches. Resumes with non-standard headers (e.g. "Work History", "Professional Background") will not be segmented correctly. Noted in `segmenter.py` comments.
- **`raw_text` not stored in DB** — `intake.py` inserts `raw_text=""` as a placeholder. The actual parsed text should be written back to the `resumes.raw_text` column after processing.
- **Embedding deduplication** — Re-running the pipeline for the same resume inserts a new embedding row each time. Should check for existing embedding before inserting.
- **`session.py` DB URL hardcoded** — Default URL has credentials in plaintext. Should be moved to `.env` and loaded via `python-dotenv` or similar.

---

## Run Command (for reference)
```bash
set PYTHONPATH=c:\My_Programs\Job Application Agent;c:\My_Programs\Job Application Agent\backend
uv run python test_pipeline.py
# run from: Samples/sample_test/
```
