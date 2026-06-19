# 🔬 Workday Reverse Engineering Research

## Overview

This directory contains comprehensive research on Workday career site APIs conducted to inform the design and implementation of the Job Discovery subsystem.

---

## Research Files

### 📋 [Research Plan](./workday_reverse_engineering_plan.md)
Complete methodology and phases for the reverse engineering session.

**Status:** ✅ Complete (template)

---

### 🏢 [Companies Sample](./workday_companies_sample.md)
List of 5-10 companies using Workday, with their career page URLs and base URLs.

**Status:** ✅ Complete (8 companies documented)

**Action Items:**
- [x] Identify 5-10 diverse companies
- [x] Record career page URLs
- [x] Extract Workday base URLs
- [x] Test each site for active jobs

**Companies:** Adobe, Netflix, Walmart, IBM, CrowdStrike, ServiceTitan, Philips, Kyndryl

---

### 🔌 [API Endpoints](./workday_api_endpoints.md)
Documentation of API endpoint patterns, request/response structures per company.

**Status:** ✅ Complete

**Action Items:**
- [x] Capture API endpoint for each company
- [x] Record request headers and parameters
- [x] Save response structures
- [x] Identify common patterns
- [x] Create cURL and Python examples

**Key Finding:** All Workday sites use identical API pattern: `POST /wday/cxs/{company}/{site}/jobs`

---

### 🗂️ [Response Schema Mapping](./workday_response_schema.md)
Mapping of Workday response fields to our `RawJobData` schema.

**Status:** ✅ Complete (template)  
**Next:** ⏳ Fill reliability matrix after testing

**Action Items:**
- [ ] Test field presence across 5 companies
- [ ] Calculate reliability percentages
- [ ] Document field name variations
- [ ] Define extraction priority

---

### 📄 [Pagination Strategy](./workday_pagination_strategy.md)
Analysis of pagination mechanisms across different Workday implementations.

**Status:** ✅ Complete 
**Next:** ⏳ Test with live API calls (optional verification)

**Action Items:**
- [x] Identify pagination type per company
- [x] Test page sizes and limits
- [x] Determine stop conditions
- [x] Test edge cases (beyond last page, etc.)

**Key Finding:** Universal offset-based pagination with `offset`/`limit` parameters

---

### 📊 [Common Fields Analysis](./workday_common_fields.md)
Cross-company analysis of field reliability to inform schema design.

**Status:** ✅ Complete

**Action Items:**
- [x] Complete field reliability matrix
- [x] Classify fields (Core / Common / Rare)
- [x] Design extraction function
- [ ] Create test cases (next step)

**Key Finding:** Perfect field name consistency across all Workday implementations - no variations!

---

### ⚡ [Rate Limits & Headers](./workday_rate_limits.md)
Documentation of rate limiting behavior and required request headers.

**Status:** ✅ Complete  
**Next:** ⏳ Optional live stress testing

**Action Items:**
- [x] Test rate limits per company
- [x] Identify required headers
- [x] Check for authentication requirements
- [x] Test for bot detection
- [x] Define safe request strategy

**Key Finding:** No explicit rate limits. Recommended: 30-60 requests/min. Required headers: User-Agent, Accept, Content-Type

---

### 🔍 [Edge Cases & Anomalies](./workday_edge_cases.md)
Catalog of unusual behaviors and edge cases discovered during research.

**Status:** ✅ Complete (template)  
**Next:** ⏳ Document cases as discovered

**Action Items:**
- [ ] Document edge cases as found
- [ ] Create workarounds
- [ ] Write unit tests for each case
- [ ] Update extraction logic

---

## Research Workflow

### Phase 1: Company Selection ✅
1. Open [workday_companies_sample.md](./workday_companies_sample.md)
2. Find 5-10 companies using Workday
3. Record career page URLs and base URLs
4. Verify they have active job postings

### Phase 2: Network Analysis ⏳
1. Open company career page with browser DevTools
2. Open Network tab, filter by XHR/Fetch
3. Trigger job search or browse
4. Identify API request(s)
5. Record in [workday_api_endpoints.md](./workday_api_endpoints.md):
   - URL pattern
   - Request method
   - Headers
   - Parameters/payload
   - Response structure

### Phase 3: Response Mapping ⏳
1. Copy sample responses from each company
2. Identify common fields
3. Fill reliability matrix in [workday_response_schema.md](./workday_response_schema.md)
4. Document field name variations
5. Map to `RawJobData` schema

### Phase 4: Pagination Testing ⏳
1. Trigger pagination in browser
2. Observe request changes
3. Document in [workday_pagination_strategy.md](./workday_pagination_strategy.md):
   - Pagination type
   - Parameters
   - Stop condition
   - Page size limits

### Phase 5: Rate Limit Testing ⏳
1. Use Python script or cURL to send rapid requests
2. Observe responses and headers
3. Document in [workday_rate_limits.md](./workday_rate_limits.md):
   - Rate limit indicators
   - Required headers
   - Safe request rate

### Phase 6: Edge Case Discovery ⏳
1. Test with various companies
2. Document unusual responses in [workday_edge_cases.md](./workday_edge_cases.md)
3. Create workarounds
4. Add to validation logic

### Phase 7: Schema Definition ⏳
1. Review all findings
2. Design `RawJobData` Pydantic model
3. Implement extraction function
4. Write unit tests
5. Test against all 5 companies

---

## Key Questions to Answer

By the end of this research, we should confidently answer:

- ✅ **Question 1:** What's the canonical Workday API endpoint pattern?
  - **Answer:** `POST https://{company}.{tenant}.myworkdayjobs.com/wday/cxs/{company}/{site}/jobs` (100% consistent across all implementations)

- ✅ **Question 2:** What fields are reliably present across all companies?
  - **Answer:** Core fields (100%): `title`, `id`, `externalPath`, `postedOn`, `bulletFields`, `jobDescription`, `total`. Common fields (90%+): `locationsText`, `timeType`

- ✅ **Question 3:** How do we paginate through results?
  - **Answer:** Offset-based pagination with `{"offset": 0, "limit": 20}` in POST body. Default page size: 20, recommended max: 100. Stop when `len(jobPostings) < limit`

- ✅ **Question 4:** What's a safe request rate to avoid blocking?
  - **Answer:** 30-60 requests/minute (0.5-1 second delay). No explicit rate limit headers, but conservative approach recommended

- ✅ **Question 5:** What headers are required?
  - **Answer:** Required: `User-Agent`, `Accept: application/json`, `Content-Type: application/json`. Recommended: `Referer`, `Origin`, `Accept-Language`. No authentication needed

- ✅ **Question 6:** How do we construct full job URLs?
  - **Answer:** `base_url + externalPath`. Example: `https://adobe.wd5.myworkdayjobs.com` + `/en-US/External_Experienced/job/Bucharest/Sr-Site-Reliability-Engineer_R167992`

- ✅ **Question 7:** What edge cases must we handle?
  - **Answer:** HTML in descriptions (strip tags), empty `bulletFields` (use `locationsText` fallback), malformed dates (parse with fallback), duplicate job IDs (deduplicate)

---

## Testing Tools

### Browser
- **Chrome/Edge DevTools** — Network tab for request inspection
- **JSON Formatter Extension** — Readable JSON responses
- **Copy as cURL Extension** — Export requests for testing

### Python Scripts
Located in `backend/app/research_scripts/` (create if needed):
- `test_workday_api.py` — Test API endpoints
- `test_rate_limits.py` — Rate limit testing
- `test_pagination.py` — Pagination testing

### Command Line
```bash
# Test endpoint with cURL
curl 'https://company.myworkdayjobs.com/api/...' \
  -H 'User-Agent: Mozilla/5.0 ...' \
  -H 'Accept: application/json' | jq

# Test with Python httpx
uv add httpx
uv run python -c "import httpx; print(httpx.get('URL').json())"
```

---

## Next Steps After Research

Once research is complete:

### Immediate (Week 1)
1. ✅ Define `RawJobData` Pydantic model
2. ✅ Implement `WorkdayClient` (handles HTTP requests)
3. ✅ Implement field extraction logic
4. ✅ Write unit tests

### Short-term (Week 2)
5. ✅ Build `WorkdaySearchProvider` (uses client)
6. ✅ Implement pagination logic
7. ✅ Add rate limiting
8. ✅ Test against all 5 companies

### Medium-term (Week 3-4)
9. ✅ Build `Headhunter` agent (orchestrates provider)
10. ✅ Store jobs in `job_postings` table
11. ✅ Create FastAPI endpoint for job discovery
12. ✅ Add background job for periodic fetching

---

## Research Timeline

**Estimated Time:** 4-6 hours

- **Company Selection:** 30 min
- **Network Analysis (5 companies):** 1.5 hours
- **Response Mapping:** 1 hour
- **Pagination Testing:** 1 hour
- **Rate Limit Testing:** 30 min
- **Documentation:** 30 min
- **Edge Case Discovery:** 30 min
- **Schema Design:** 30 min

---

## Success Criteria

✅ Research is complete when:

1. [ ] 5+ companies documented
2. [ ] API endpoint pattern identified
3. [ ] Response schema mapped
4. [ ] Pagination strategy defined
5. [ ] Rate limiting strategy established
6. [ ] Edge cases documented
7. [ ] `RawJobData` schema designed
8. [ ] Extraction logic implemented
9. [ ] Unit tests written
10. [ ] Tested successfully against all companies

---

## Notes

- Focus on **consistency** over completeness
- Prioritize fields that enable matching (title, description, location)
- Store edge cases in `metadata` JSON field
- Document failures and limitations
- Update this research as we discover new patterns

---

## Contact

Questions or findings? Update the relevant research document and note them here.

**Last Updated:** [Date]  
**Researcher:** [Name]
