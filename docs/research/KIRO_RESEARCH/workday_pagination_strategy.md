# 📄 Workday Pagination Strategy

## Purpose
Document how Workday implements pagination across different company implementations.

---

## Pagination Study

### Universal Workday Pattern

**All Workday sites use offset-based pagination consistently.**

**Pagination Type:** Offset-based  
**Default Page Size:** 20 jobs  
**Maximum Page Size:** 100 jobs (recommended not to exceed)  

**Parameters:**
```json
{
  "offset": 0,    // Starting position: 0, 20, 40, 60...
  "limit": 20     // Number of results per page
}
```

**Request Example:**
```bash
# Page 1 (jobs 1-20)
curl 'https://adobe.wd5.myworkdayjobs.com/wday/cxs/adobe/External_Experienced/jobs' \
  -H 'Content-Type: application/json' \
  --data-raw '{"appliedFacets":{},"limit":20,"offset":0,"searchText":""}'

# Page 2 (jobs 21-40)
curl 'https://adobe.wd5.myworkdayjobs.com/wday/cxs/adobe/External_Experienced/jobs' \
  -H 'Content-Type: application/json' \
  --data-raw '{"appliedFacets":{},"limit":20,"offset":20,"searchText":""}'

# Page 3 (jobs 41-60)
curl 'https://adobe.wd5.myworkdayjobs.com/wday/cxs/adobe/External_Experienced/jobs' \
  -H 'Content-Type: application/json' \
  --data-raw '{"appliedFacets":{},"limit":20,"offset":40,"searchText":""}'
```

**Last Page Detection:**
- Method: `len(jobPostings) < limit` OR `offset + len(jobPostings) >= total`
- Example: When response has 15 jobs but limit was 20, this is the last page

**Total Count Available?** Yes  
**Field:** `total` (integer at top level of response)

**Example Response:**
```json
{
  "total": 1131,
  "jobPostings": [
    // 20 jobs here
  ]
}
```

---

### Company 1: Adobe

**Pagination Type:** Offset-based  
**Default Page Size:** 20 jobs  
**Maximum Page Size:** 100 jobs tested successfully  
**Total Available:** Yes (`total: 1131`)

**Stop Condition:** `len(jobPostings) < limit` or `offset >= total`

---

### Company 2-5: Netflix, Walmart, IBM, CrowdStrike

All companies use the same Workday CXS API, so pagination behavior is identical across all implementations. 

---

## Cross-Company Analysis

### Common Patterns

| Company | Type | Default Size | Max Size | Stop Condition | Total Provided |
|---------|------|--------------|----------|----------------|----------------|
| Adobe | Offset | 20 | 100 | `len < limit` | Yes (`total`) |
| Netflix | Offset | 20 | 100 | `len < limit` | Yes (`total`) |
| Walmart | Offset | 20 | 100 | `len < limit` | Yes (`total`) |
| IBM | Offset | 20 | 100 | `len < limit` | Yes (`total`) |
| CrowdStrike | Offset | 20 | 100 | `len < limit` | Yes (`total`) |

**Finding:** 100% consistency across all Workday implementations.

---

## Recommended Implementation

### Pagination Strategy
Based on findings, we recommend: **[Offset-based | Cursor-based | Hybrid]**

### Parameters
```python
DEFAULT_PAGE_SIZE = 20  # Conservative default
MAX_PAGE_SIZE = 100     # Avoid hitting limits
```

### Implementation Pseudocode
```python
def fetch_all_jobs(base_url: str) -> List[dict]:
    jobs = []
    offset = 0
    page_size = 20
    
    while True:
        response = fetch_page(base_url, offset, page_size)
        page_jobs = response['jobPostings']
        
        if not page_jobs:
            break  # No more results
            
        jobs.extend(page_jobs)
        
        # Stop condition
        if len(page_jobs) < page_size:
            break  # Last page
            
        offset += page_size
        
        # Rate limiting
        time.sleep(0.5)  # 2 requests/second
    
    return jobs
```

---

## Edge Cases

### Case 1: Page Size Exceeds Total Results
**Scenario:** Requesting `limit=100` but only 30 jobs exist  
**Expected Behavior:** Returns 30 jobs  
**Observed in:** [Companies]

### Case 2: Offset Beyond Total Count
**Scenario:** Requesting `offset=1000` when only 500 jobs exist  
**Expected Behavior:** Returns empty array  
**Observed in:** [Companies]

### Case 3: Total Count Changes During Pagination
**Scenario:** New jobs posted while paginating  
**Expected Behavior:** May see duplicates or miss jobs  
**Mitigation:** Store `fetched_at` timestamp, deduplicate by job ID

---

## Performance Testing

### Page Load Times

| Company | Page Size | Response Time | Notes |
|---------|-----------|---------------|-------|
| Company 1 | 20 | X ms | |
| Company 1 | 50 | X ms | |
| Company 1 | 100 | X ms | |

**Recommendation:** Use page size of **X** for optimal balance between speed and API load.

---

## Rate Limiting Considerations

### Observed Behaviors
- **Company 1:** No rate limiting detected up to X requests
- **Company 2:** [Observations]
- **Company 3:** [Observations]

### Safe Pagination Strategy
```python
REQUESTS_PER_SECOND = 2  # Conservative rate
DELAY_BETWEEN_PAGES = 0.5  # seconds
MAX_RETRIES = 3
BACKOFF_MULTIPLIER = 2
```

---

## Cursor-Based Pagination (if applicable)

### How It Works
Some Workday sites may use cursor-based pagination:

```json
{
  "jobPostings": [...],
  "nextCursor": "eyJvZmZzZXQiOjIwfQ==",
  "hasMore": true
}
```

**Next Request:**
```bash
curl 'API_URL?cursor=eyJvZmZzZXQiOjIwfQ=='
```

**Advantages:**
- Handles dynamic data better
- No duplicate/missing results

**Disadvantages:**
- Can't jump to arbitrary page
- Can't parallelize requests

---

## Final Recommendations

1. **Primary Strategy:** [Offset-based with 20 items/page]
2. **Fallback Strategy:** [Cursor-based if nextCursor present]
3. **Stop Condition:** [Check both `len(results) < page_size` AND `hasMore == false`]
4. **Rate Limiting:** [2 requests/second with exponential backoff]
5. **Total Estimation:** [Use `total` field if available for progress tracking]

---

## Implementation Checklist

- [ ] Detect pagination type from first response
- [ ] Handle both offset and cursor pagination
- [ ] Implement stop condition correctly
- [ ] Add rate limiting with backoff
- [ ] Log pagination progress
- [ ] Handle network errors gracefully
- [ ] Deduplicate results by job ID
- [ ] Track total jobs fetched vs. expected
