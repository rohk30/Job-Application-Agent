# 🔬 Workday API Reverse Engineering — Research Plan

## 📋 Session Goal

**Answer:** Given any Workday company site, how do we consistently extract open jobs?

This research will directly inform:
- `RawJobData` schema design
- `WorkdaySearchProvider` implementation
- Headhunter agent subsystem architecture

---

## 🎯 Research Phases

### Phase 1: Sample Collection (5-10 Companies)

Collect diverse Workday implementations to identify patterns and edge cases.

**Target Companies:**
1. [ ] Company 1
2. [ ] Company 2
3. [ ] Company 3
4. [ ] Company 4
5. [ ] Company 5
6. [ ] Company 6 (optional)
7. [ ] Company 7 (optional)
8. [ ] Company 8 (optional)
9. [ ] Company 9 (optional)
10. [ ] Company 10 (optional)

**For Each Company Record:**
- `company_name`: Full company name
- `career_page`: Public-facing URL
- `base_url`: Workday tenant base URL

---

### Phase 2: Network Traffic Analysis

**Steps:**
1. Open career page with DevTools (Network tab)
2. Clear network log
3. Trigger job search / browse
4. Identify the API endpoint(s)

**Capture:**
- Request URL pattern
- Request method (GET/POST)
- Query parameters or POST payload
- Required headers
- Response structure

**Record in:** `docs/research/workday_api_endpoints.md`

---

### Phase 3: Response Schema Mapping

**Goal:** Map Workday response fields → our `RawJobData` model

**Deliverable:** `docs/research/workday_response_schema.md`

**Example Structure:**

| Workday Field | Type | Meaning | RawJobData Field | Notes |
|---------------|------|---------|------------------|-------|
| `title` | string | Job title | `title` | Always present |
| `externalPath` | string | Job URL suffix | `raw_url` | Needs base URL prefix |
| `bulletFields[0]` | string | Location | `location` | Array index may vary |
| `postedOn` | string | Posted date | `posted_at` | ISO 8601 format |
| `jobDescription` | string | Full description | `job_description` | May contain HTML |

---

### Phase 4: Pagination Study

**Questions to Answer:**
- Is pagination offset-based, cursor-based, or page-based?
- What parameters control pagination?
- What's the default page size?
- What's the maximum page size?
- How do we detect the last page?
- Are there rate limits per page request?

**Deliverable:** `docs/research/workday_pagination_strategy.md`

---

### Phase 5: Common Fields Analysis

**Goal:** Identify fields present across ALL companies (reliable) vs. optional

**Deliverable:** `docs/research/workday_common_fields.md`

**Format:**

| Field | Company 1 | Company 2 | Company 3 | Company 4 | Company 5 | Reliability |
|-------|-----------|-----------|-----------|-----------|-----------|-------------|
| `title` | ✅ | ✅ | ✅ | ✅ | ✅ | 100% |
| `location` | ✅ | ✅ | ✅ | ✅ | ❌ | 80% |
| `salary` | ❌ | ❌ | ✅ | ❌ | ❌ | 20% |

**Classification:**
- **Core (100%)** — Always present, required for `RawJobData`
- **Common (60-99%)** — Usually present, make optional
- **Rare (<60%)** — Edge case, store in `metadata` JSON field

---

### Phase 6: Rate Limiting & Headers Study

**Investigate:**
- Are API keys required?
- Is authentication needed?
- Are there rate limit headers (`X-RateLimit-*`)?
- What's a safe request cadence?
- Do requests need specific `User-Agent` or other headers?
- Are there CORS restrictions (would affect browser-based scraping)?

**Deliverable:** `docs/research/workday_rate_limits.md`

---

### Phase 7: Formal Schema Definition

**Only AFTER completing Phases 1-6.**

**Deliverable:** `backend/app/domain/entities/raw_job_data.py`

```python
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class RawJobData(BaseModel):
    """
    Normalized representation of a job extracted from Workday.
    
    Based on reverse engineering of N=5 Workday implementations.
    See: docs/research/workday_common_fields.md
    """
    
    # Core fields (100% reliability)
    title: str
    raw_url: str  # Reconstructed from externalPath + base_url
    posted_at: datetime
    
    # Common fields (>60% reliability)
    location: Optional[str] = None
    job_description: Optional[str] = None
    
    # Metadata (catch-all for variable fields)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Provenance tracking
    source: str = "workday"
    company_name: str
    fetched_at: datetime
```

---

## 📝 Research Files to Create

1. `docs/research/workday_companies_sample.md` — Company list + URLs
2. `docs/research/workday_api_endpoints.md` — Endpoint patterns per company
3. `docs/research/workday_response_schema.md` — Field mapping table
4. `docs/research/workday_pagination_strategy.md` — Pagination analysis
5. `docs/research/workday_common_fields.md` — Cross-company field reliability
6. `docs/research/workday_rate_limits.md` — Rate limiting findings
7. `docs/research/workday_edge_cases.md` — Weird stuff we found

---

## 🧪 Tools & Setup

**Browser:** Chrome/Edge with DevTools
**Extensions:** 
- JSON Formatter (for readable responses)
- Copy as cURL (for request reproduction)

**Python Testing:**
```bash
# After capturing requests, test with:
uv add httpx
uv run python -c "import httpx; ..."
```

---

## ✅ Success Criteria

By end of session, we should be able to answer:

1. ✅ What's the canonical Workday API endpoint pattern?
2. ✅ What fields are reliably available across companies?
3. ✅ How do we paginate through results?
4. ✅ What's the rate limit strategy?
5. ✅ Can we confidently design `RawJobData` schema?

---

## 🚀 Next Steps After Research

Once research is complete:

1. Implement `RawJobData` schema
2. Build `WorkdayClient` (handles API requests)
3. Build `WorkdaySearchProvider` (uses client, returns `RawJobData`)
4. Build `Headhunter` agent (orchestrates provider)
5. Store jobs in `job_postings` table
6. Test with real companies

---

## 📌 Notes

- Focus on consistency over completeness
- Edge cases go in `metadata` field
- Prioritize fields that enable matching (title, description, location)
- Document failures and limitations

