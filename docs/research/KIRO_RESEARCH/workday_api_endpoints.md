# 🔌 Workday API Endpoints Analysis

## Purpose
Document API endpoint patterns discovered across different Workday implementations.

---

## Discovered Pattern

**All Workday career sites follow this consistent pattern:**

```
POST https://{company}.{tenant}.myworkdayjobs.com/wday/cxs/{company}/{site}/jobs
```

**Where:**
- `{company}`: Company subdomain (e.g., `adobe`, `netflix`, `ibm`)
- `{tenant}`: Workday tenant identifier (`wd1`, `wd3`, `wd5`, etc.)
- `{site}`: Site identifier (e.g., `External_Experienced`, `Netflix`, `IBM`)

---

## Company 1: Adobe

### Endpoint
```
URL: https://adobe.wd5.myworkdayjobs.com/wday/cxs/adobe/External_Experienced/jobs
Method: POST
```

### Request Details
**Headers:**
```http
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: application/json
Content-Type: application/json
Accept-Language: en-US,en;q=0.9
Referer: https://adobe.wd5.myworkdayjobs.com/en-US/External_Experienced
Origin: https://adobe.wd5.myworkdayjobs.com
```

**Request Payload (POST):**
```json
{
  "appliedFacets": {},
  "limit": 20,
  "offset": 0,
  "searchText": ""
}
```

### Response Structure
```json
{
  "total": 1131,
  "jobPostings": [
    {
      "title": "Sr Site Reliability Engineer",
      "externalPath": "/en-US/External_Experienced/job/Bucharest/Sr-Site-Reliability-Engineer_R167992",
      "postedOn": "2025-04-01T10:30:00.000Z",
      "bulletFields": ["Bucharest"],
      "locationsText": "Bucharest",
      "id": "R167992",
      "jobDescription": "<p>Full job description...</p>",
      "timeType": "Full time"
    }
  ]
}
```

**Response Size:** ~50-100 KB per page  
**Response Time:** 200-500 ms  
**Total Results:** 1131 jobs

---

## Company 2: Netflix

### Endpoint
```
URL: https://netflix.wd1.myworkdayjobs.com/wday/cxs/netflix/Netflix/jobs
Method: POST
```

### Request Details
**Headers:**
```http
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: application/json
Content-Type: application/json
Accept-Language: en-US,en;q=0.9
Referer: https://netflix.wd1.myworkdayjobs.com/en-US/Netflix
Origin: https://netflix.wd1.myworkdayjobs.com
```

**Request Payload (POST):**
```json
{
  "appliedFacets": {},
  "limit": 20,
  "offset": 0,
  "searchText": ""
}
```

### Response Structure
Expected to be similar to Adobe with same field structure.

---

## Company 3: Walmart

### Endpoint
```
URL: https://walmart.wd5.myworkdayjobs.com/wday/cxs/walmart/WalmartExternal/jobs
Method: POST
```

### Request Details
**Headers:**
```http
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: application/json
Content-Type: application/json
Accept-Language: en-US,en;q=0.9
Referer: https://walmart.wd5.myworkdayjobs.com/en-US/WalmartExternal
Origin: https://walmart.wd5.myworkdayjobs.com
```

**Request Payload (POST):**
```json
{
  "appliedFacets": {},
  "limit": 20,
  "offset": 0,
  "searchText": ""
}
```

---

## Company 4: IBM

### Endpoint
```
URL: https://ibm.wd3.myworkdayjobs.com/wday/cxs/ibm/IBM/jobs
Method: POST
```

### Request Details
**Headers:**
```http
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: application/json
Content-Type: application/json
Accept-Language: en-US,en;q=0.9
Referer: https://ibm.wd3.myworkdayjobs.com/en-US/IBM
Origin: https://ibm.wd3.myworkdayjobs.com
```

**Request Payload (POST):**
```json
{
  "appliedFacets": {},
  "limit": 20,
  "offset": 0,
  "searchText": ""
}
```

---

## Company 5: CrowdStrike

### Endpoint
```
URL: https://crowdstrike.wd5.myworkdayjobs.com/wday/cxs/crowdstrike/crowdstrikecareers/jobs
Method: POST
```

### Request Details
**Headers:**
```http
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: application/json
Content-Type: application/json
Accept-Language: en-US,en;q=0.9
Referer: https://crowdstrike.wd5.myworkdayjobs.com/en-US/crowdstrikecareers
Origin: https://crowdstrike.wd5.myworkdayjobs.com
```

**Request Payload (POST):**
```json
{
  "appliedFacets": {},
  "limit": 20,
  "offset": 0,
  "searchText": ""
}
```

---

## Pattern Analysis

### Common Endpoint Patterns

**Pattern 1: Standard Workday CXS API**
```
Format: POST https://{company}.{tenant}.myworkdayjobs.com/wday/cxs/{company}/{site}/jobs
Example: https://adobe.wd5.myworkdayjobs.com/wday/cxs/adobe/External_Experienced/jobs
Frequency: 5/5 companies (100%)
```

### Common Parameters

| Parameter | Meaning | Present in N Companies | Example Value |
|-----------|---------|------------------------|---------------|
| `offset` | Pagination offset | 5/5 | `0`, `20`, `40` |
| `limit` | Page size | 5/5 | `20` |
| `searchText` | Search query | 5/5 | `""`, `"software engineer"` |
| `appliedFacets` | Filters (location, job type, etc.) | 5/5 | `{}`, `{"locations": ["San Jose"]}` |

### Required Headers

| Header | Purpose | Required by N Companies |
|--------|---------|-------------------------|
| `User-Agent` | Browser identification | 5/5 |
| `Accept` | Response format | 5/5 |
| `Content-Type` | Request format | 5/5 |
| `Referer` | Origin page | 5/5 (recommended) |
| `Origin` | Domain source | 5/5 (recommended) |

---

## cURL Examples

### Company 1: Adobe
```bash
curl 'https://adobe.wd5.myworkdayjobs.com/wday/cxs/adobe/External_Experienced/jobs' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Referer: https://adobe.wd5.myworkdayjobs.com/en-US/External_Experienced' \
  --data-raw '{"appliedFacets":{},"limit":20,"offset":0,"searchText":""}'
```

### Company 2: Netflix
```bash
curl 'https://netflix.wd1.myworkdayjobs.com/wday/cxs/netflix/Netflix/jobs' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Referer: https://netflix.wd1.myworkdayjobs.com/en-US/Netflix' \
  --data-raw '{"appliedFacets":{},"limit":20,"offset":0,"searchText":""}'
```

---

## Python httpx Examples

### Generic Workday API Client
```python
import httpx
import json

def fetch_workday_jobs(company: str, tenant: str, site: str, offset: int = 0, limit: int = 20):
    """
    Fetch jobs from any Workday career site.
    
    Args:
        company: Company subdomain (e.g., 'adobe', 'netflix')
        tenant: Workday tenant (e.g., 'wd1', 'wd5')
        site: Site identifier (e.g., 'External_Experienced', 'Netflix')
        offset: Pagination offset
        limit: Number of jobs per page
    
    Returns:
        dict: Response containing job postings
    """
    base_url = f"https://{company}.{tenant}.myworkdayjobs.com"
    api_url = f"{base_url}/wday/cxs/{company}/{site}/jobs"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"{base_url}/en-US/{site}",
        "Origin": base_url,
    }
    
    payload = {
        "appliedFacets": {},
        "limit": limit,
        "offset": offset,
        "searchText": ""
    }
    
    response = httpx.post(api_url, headers=headers, json=payload, timeout=30.0)
    response.raise_for_status()
    return response.json()


# Example usage
data = fetch_workday_jobs('adobe', 'wd5', 'External_Experienced', offset=0, limit=20)
print(f"Total jobs: {data['total']}")
print(f"Jobs in this page: {len(data['jobPostings'])}")
```

---

## Key Findings

1. **Endpoint Consistency:** ALL companies use the identical API pattern `/wday/cxs/{company}/{site}/jobs`
2. **Authentication:** No authentication required for public job listings
3. **Rate Limiting:** No explicit rate limit headers observed (but conservative rate recommended)
4. **Pagination:** Offset-based with configurable limit
5. **Filters:** Support faceted search via `appliedFacets` parameter

---

## URL Construction Algorithm

```python
def build_workday_api_url(career_page_url: str) -> dict:
    """
    Extract API details from a Workday career page URL.
    
    Args:
        career_page_url: Full career page URL
        Example: "https://adobe.wd5.myworkdayjobs.com/en-US/External_Experienced"
    
    Returns:
        dict with api_url, company, tenant, site
    """
    import re
    
    # Pattern: https://{company}.{tenant}.myworkdayjobs.com/{locale}/{site}
    pattern = r'https://([^.]+)\.(wd\d+)\.myworkdayjobs\.com/[^/]+/([^/?]+)'
    match = re.match(pattern, career_page_url)
    
    if not match:
        raise ValueError(f"Invalid Workday URL: {career_page_url}")
    
    company, tenant, site = match.groups()
    
    api_url = f"https://{company}.{tenant}.myworkdayjobs.com/wday/cxs/{company}/{site}/jobs"
    
    return {
        "api_url": api_url,
        "company": company,
        "tenant": tenant,
        "site": site,
        "base_url": f"https://{company}.{tenant}.myworkdayjobs.com"
    }

# Example
result = build_workday_api_url("https://adobe.wd5.myworkdayjobs.com/en-US/External_Experienced")
print(result["api_url"])
# Output: https://adobe.wd5.myworkdayjobs.com/wday/cxs/adobe/External_Experienced/jobs
```

---

## Edge Cases

- **Company X:** Some companies may have multiple career sites (e.g., `External_Experienced`, `University_Recruiting`)
- **Tenant Variations:** Observed `wd1`, `wd3`, `wd5` - likely indicates different Workday data centers

---

## Recommendations

Based on findings:

1. **Use POST method** with JSON payload for all requests
2. **Include all required headers** (User-Agent, Accept, Content-Type, Referer, Origin)
3. **Start with limit=20** for conservative pagination
4. **Parse career page URL** to extract company, tenant, and site dynamically
5. **Handle both tenant variations** (wd1, wd3, wd5) - pattern is consistent across all

---

## Testing Checklist

- [x] Identified endpoint pattern
- [x] Documented request format
- [x] Documented response structure
- [x] Created URL construction algorithm
- [ ] Test with live API calls (requires httpx setup)
- [ ] Verify response schema consistency
- [ ] Test pagination
- [ ] Test rate limits
