# 🔍 Workday Edge Cases & Anomalies

## Purpose
Document unusual behaviors, edge cases, and anomalies discovered during reverse engineering.

---

## Edge Case 1: [TITLE]

**Company:** [NAME]  
**Date Discovered:** 

### Description
[Detailed description of the edge case]

### Example
```json
{
  "example": "data showing the edge case"
}
```

### Impact
- **Severity:** Low | Medium | High | Critical
- **Affects:** Pagination | Field extraction | Rate limiting | Other
- **Frequency:** Rare | Occasional | Common

### Workaround
```python
# Code showing how to handle this case
```

### Recommendation
[How to handle in production code]

---

## Edge Case 2: [TITLE]

**Company:** [NAME]  
**Date Discovered:** 

### Description

### Example
```json

```

### Impact
- **Severity:** 
- **Affects:** 
- **Frequency:** 

### Workaround
```python

```

### Recommendation

---

## Common Edge Cases to Watch For

### 1. Empty Job Descriptions
**Symptom:** `jobDescription` field is empty string or null  
**Frequency:** [X% of jobs]  
**Companies:** [List]

**Handling:**
```python
description = job.get('jobDescription', '').strip()
if not description:
    logger.warning(f"Empty description for job {job['id']}")
    description = job.get('summary', 'No description provided')
```

---

### 2. Missing Location Data
**Symptom:** No location field (bulletFields empty, locationsText null)  
**Frequency:** [X% of jobs]  
**Companies:** [List]

**Possible Reasons:**
- Remote position with no specified location
- Location to be determined
- Data error

**Handling:**
```python
location = extract_location(job)
if not location:
    location = "Location not specified"
    metadata['location_missing'] = True
```

---

### 3. Malformed Dates
**Symptom:** Date in unexpected format or invalid value  
**Examples:**
- `"Posted just now"`
- `"2024-13-45"` (invalid date)
- `"TBD"`

**Handling:**
```python
def parse_posted_date(date_str: str) -> datetime:
    try:
        # Try ISO format
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except ValueError:
        # Try other common formats
        for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y']:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        # Fallback to current time
        logger.warning(f"Could not parse date: {date_str}")
        return datetime.now(timezone.utc)
```

---

### 4. HTML in Job Titles
**Symptom:** Job title contains HTML tags  
**Example:** `"<span>Senior</span> Software Engineer"`

**Handling:**
```python
from html import unescape
import re

def clean_title(title: str) -> str:
    # Remove HTML tags
    title = re.sub(r'<[^>]+>', '', title)
    # Unescape entities
    title = unescape(title)
    # Clean whitespace
    return title.strip()
```

---

### 5. Duplicate Jobs in Response
**Symptom:** Same job ID appears multiple times in single response  
**Frequency:** [Rare | Occasional | Common]  
**Companies:** [List]

**Possible Reasons:**
- Job posted in multiple locations
- Job posted in multiple categories
- API bug

**Handling:**
```python
# Deduplicate by job ID
seen_ids = set()
unique_jobs = []
for job in jobs:
    job_id = job.get('id')
    if job_id not in seen_ids:
        seen_ids.add(job_id)
        unique_jobs.append(job)
    else:
        logger.debug(f"Duplicate job ID: {job_id}")
```

---

### 6. Very Long Job Descriptions
**Symptom:** Description > 50,000 characters  
**Impact:** Database storage, embedding generation time

**Handling:**
```python
MAX_DESCRIPTION_LENGTH = 50000

description = job.get('jobDescription', '')
if len(description) > MAX_DESCRIPTION_LENGTH:
    logger.warning(f"Truncating long description for job {job['id']}")
    description = description[:MAX_DESCRIPTION_LENGTH] + "...[truncated]"
```

---

### 7. Special Characters in Job IDs
**Symptom:** Job ID contains `/`, `?`, `#`, or other URL-unsafe characters  
**Example:** `"JR-2024/03/12345"`

**Impact:** URL construction, database keys

**Handling:**
```python
from urllib.parse import quote

job_id = job.get('id')
safe_job_id = quote(job_id, safe='')  # URL-encode
```

---

### 8. Pagination Returns Duplicate Results
**Symptom:** Jobs from page 2 overlap with page 1  
**Cause:** New jobs posted during pagination

**Handling:**
```python
# Track all fetched job IDs
all_job_ids = set()

for page in paginate():
    for job in page:
        job_id = job.get('id')
        if job_id in all_job_ids:
            logger.debug(f"Skipping duplicate: {job_id}")
            continue
        all_job_ids.add(job_id)
        yield job
```

---

### 9. Inconsistent Total Count
**Symptom:** `total` field changes between pagination requests  
**Example:** Page 1 says 100 jobs, page 2 says 105 jobs

**Handling:**
```python
# Don't rely on total for stop condition
# Use empty results as stop condition instead
if not page_results:
    break
```

---

### 10. Missing `externalPath`
**Symptom:** No URL path provided for job  
**Frequency:** [Very rare]

**Possible Workaround:**
```python
# Construct URL from job ID if externalPath missing
if not job.get('externalPath'):
    job_id = job.get('id')
    # Common Workday URL pattern
    path = f"/en-US/job/Job/{job_id}"
    logger.warning(f"Constructed path for job {job_id}")
```

---

### 11. Jobs with No Posted Date
**Symptom:** `postedOn` field missing or null

**Handling:**
```python
posted_at = job.get('postedOn')
if not posted_at:
    # Use current timestamp as fallback
    posted_at = datetime.now(timezone.utc)
    metadata['posted_date_assumed'] = True
```

---

### 12. Nested or Structured Location Data
**Symptom:** Location is not a simple string

**Example:**
```json
{
  "location": {
    "city": "San Francisco",
    "state": "CA",
    "country": "USA",
    "remote": false
  }
}
```

**Handling:**
```python
def extract_location(job: dict) -> str:
    loc = job.get('location')
    
    if isinstance(loc, str):
        return loc
    
    if isinstance(loc, dict):
        parts = [
            loc.get('city'),
            loc.get('state'),
            loc.get('country')
        ]
        return ', '.join(filter(None, parts))
    
    # Fallback to bulletFields
    return (job.get('bulletFields') or [None])[0]
```

---

### 13. Rate Limit Without Retry-After Header
**Symptom:** 429 response but no `Retry-After` header

**Handling:**
```python
if response.status_code == 429:
    retry_after = int(response.headers.get('Retry-After', 60))
    # Default to 60 seconds if header missing
    logger.warning(f"Rate limited, waiting {retry_after}s")
    time.sleep(retry_after)
```

---

### 14. Jobs Posted in the Future
**Symptom:** `postedOn` date is in the future

**Example:** `"2025-12-31T00:00:00Z"` when current date is 2024-04-03

**Possible Reasons:**
- Timezone confusion
- Scheduled posting
- Data error

**Handling:**
```python
posted_at = parse_date(job['postedOn'])
now = datetime.now(timezone.utc)

if posted_at > now:
    logger.warning(f"Future posted date for job {job['id']}: {posted_at}")
    # Use current time instead
    posted_at = now
```

---

### 15. Currency Symbols in Text Fields
**Symptom:** Title or description contains salary info with currency symbols

**Example:** `"Software Engineer - $120K-150K"`

**Impact:** May affect text search/matching

**Handling:**
```python
# Normalize or remove currency symbols if needed
# Or store as-is and handle in matching logic
```

---

## Company-Specific Anomalies

### Company 1: [NAME]
**Anomaly:** [Description]  
**Workaround:** [Code or strategy]

---

### Company 2: [NAME]
**Anomaly:** [Description]  
**Workaround:** [Code or strategy]

---

## Data Quality Issues

### Observed Issues

| Issue | Frequency | Severity | Companies Affected |
|-------|-----------|----------|-------------------|
| Empty descriptions | X% | Medium | Company 1, 3 |
| Missing locations | X% | Low | Company 2 |
| Malformed dates | X% | Low | All |
| Duplicate results | X% | Low | Company 4 |

---

## Validation Rules

Based on edge cases discovered, implement these validations:

```python
def validate_job_data(job: dict) -> bool:
    """
    Validate job data before processing.
    Returns True if valid, False if should be skipped.
    """
    # Required fields
    if not job.get('title'):
        logger.error("Missing title")
        return False
    
    if not job.get('id'):
        logger.error("Missing job ID")
        return False
    
    # Title sanity check
    title = job['title']
    if len(title) > 500:
        logger.warning(f"Unusually long title: {len(title)} chars")
        return False
    
    if len(title) < 3:
        logger.warning(f"Unusually short title: {title}")
        return False
    
    # Date validation
    posted_date = job.get('postedOn')
    if posted_date:
        try:
            dt = parse_date(posted_date)
            # Check if date is reasonable (not too far in past/future)
            now = datetime.now(timezone.utc)
            if dt > now + timedelta(days=30):
                logger.warning(f"Future posted date: {dt}")
                return False
            if dt < now - timedelta(days=365):
                logger.warning(f"Very old posting: {dt}")
                # Don't reject, but flag
        except ValueError:
            logger.warning(f"Invalid date format: {posted_date}")
    
    return True
```

---

## Defensive Coding Practices

### Always Provide Defaults
```python
# Bad
location = job['location']

# Good
location = job.get('location', 'Not specified')
```

### Safe Array Access
```python
# Bad
first_bullet = job['bulletFields'][0]

# Good
bullets = job.get('bulletFields', [])
first_bullet = bullets[0] if bullets else None
```

### Type Checking
```python
# Check types before operations
description = job.get('jobDescription')
if description and isinstance(description, str):
    cleaned = strip_html(description)
```

### Graceful Degradation
```python
# If preferred field missing, try alternatives
location = (
    job.get('location') or
    job.get('locationsText') or
    (job.get('bulletFields', []) or [None])[0] or
    'Location not specified'
)
```

---

## Testing Strategy

Create test cases for all documented edge cases:

```python
# tests/test_workday_edge_cases.py

def test_empty_description():
    job = {'title': 'Test', 'id': '123', 'jobDescription': ''}
    result = extract_job_data(job)
    assert result.job_description == 'No description provided'

def test_malformed_date():
    job = {'title': 'Test', 'id': '123', 'postedOn': 'invalid'}
    result = extract_job_data(job)
    assert result.posted_at is not None  # Should not crash

def test_missing_location():
    job = {'title': 'Test', 'id': '123'}
    result = extract_job_data(job)
    assert result.location == 'Location not specified'

# ... more tests for each edge case
```

---

## Summary

**Key Takeaways:**
1. Always use `.get()` with defaults, never direct dictionary access
2. Validate all date strings before parsing
3. Strip HTML from text fields
4. Deduplicate by job ID
5. Handle missing optional fields gracefully
6. Log warnings for unexpected data
7. Don't trust `total` count for pagination stop condition
8. Implement comprehensive validation before storing

**Next Steps:**
1. ✅ Document edge cases as discovered
2. ⏳ Implement robust extraction function
3. ⏳ Write comprehensive unit tests
4. ⏳ Test against real data from all 5 companies
5. ⏳ Monitor production for new edge cases
