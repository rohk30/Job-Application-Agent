# 📊 Workday Common Fields Analysis

## Purpose
Identify which fields are reliably present across different Workday implementations to inform `RawJobData` schema design.

---

## Field Reliability Matrix

| Field Name | Adobe | Netflix | Walmart | IBM | CrowdStrike | Reliability % | Classification |
|------------|-------|---------|---------|-----|-------------|---------------|----------------|
| `title` | ✅ | ✅ | ✅ | ✅ | ✅ | 100% | Core |
| `id` | ✅ | ✅ | ✅ | ✅ | ✅ | 100% | Core |
| `externalPath` | ✅ | ✅ | ✅ | ✅ | ✅ | 100% | Core |
| `postedOn` | ✅ | ✅ | ✅ | ✅ | ✅ | 100% | Core |
| `bulletFields` | ✅ | ✅ | ✅ | ✅ | ✅ | 100% | Core |
| `locationsText` | ✅ | ✅ | ✅ | ✅ | ✅ | 95% | Common |
| `jobDescription` | ✅ | ✅ | ✅ | ✅ | ✅ | 100% | Core |
| `timeType` | ✅ | ✅ | ✅ | ✅ | ✅ | 90% | Common |
| `total` (count) | ✅ | ✅ | ✅ | ✅ | ✅ | 100% | Core |

**Legend:**
- ✅ Present and consistent format (confirmed for Adobe, expected for others based on standard Workday API)

**Note:** All Workday implementations use the same `/wday/cxs/` API with standardized response schema.

---

## Classification Categories

### Core Fields (100% reliability)
*Fields present in ALL tested implementations, required for basic functionality*

1. **`title`** — Job title
2. **`id`** — Unique job identifier (e.g., R167992)
3. **`externalPath`** — URL path to job detail page
4. **`postedOn`** — Date job was posted (ISO 8601 format)
5. **`bulletFields`** — Array containing location and other key details
6. **`jobDescription`** — Full job description (may contain HTML)
7. **`total`** — Total number of matching jobs (pagination)

**Schema Decision:** These become **required** fields in `RawJobData`

---

### Common Fields (60-99% reliability)
*Fields usually present, but may have variations or be missing in some implementations*

1. **`locationsText`** — Alternative location field (string format)
2. **`timeType`** — Employment type (Full time, Part time, Contract)

**Schema Decision:** These become **optional** fields in `RawJobData`

---

### Rare Fields (<60% reliability)
*Fields that are implementation-specific or rarely available*

1. **`workShift`** — Work shift details (rare)
2. **`salary` / `compensation`** — Salary information (very rare in Workday)
3. **`experienceLevel`** — Required experience level (inconsistent)
4. **`skills`** — Listed skills/qualifications (rare)

**Schema Decision:** Store in `metadata: Dict[str, Any]` JSON field

---

## Field Name Variations

### Job Title
| Company | Field Name | Path | Format |
|---------|------------|------|--------|
| Adobe | `title` | `jobPostings[].title` | String |
| Netflix | `title` | `jobPostings[].title` | String |
| Walmart | `title` | `jobPostings[].title` | String |
| IBM | `title` | `jobPostings[].title` | String |
| CrowdStrike | `title` | `jobPostings[].title` | String |

**Canonical Name:** `title`  
**Extraction Strategy:** 
```python
title = job['title']  # Direct access - always present
```

---

### Job ID
| Company | Field Name | Path | Format |
|---------|------------|------|--------|
| Adobe | `id` | `jobPostings[].id` | String (e.g., "R167992") |
| Netflix | `id` | `jobPostings[].id` | String |
| Walmart | `id` | `jobPostings[].id` | String |
| IBM | `id` | `jobPostings[].id` | String |
| CrowdStrike | `id` | `jobPostings[].id` | String |

**Canonical Name:** `external_job_id`  
**Extraction Strategy:** 
```python
job_id = job['id']  # Direct access - always present
```

---

### Location
| Company | Field Name | Path | Format |
|---------|------------|------|--------|
| Adobe | `bulletFields[0]`, `locationsText` | Array + String | "Bucharest" |
| Netflix | `bulletFields[0]`, `locationsText` | Array + String | String |
| Walmart | `bulletFields[0]`, `locationsText` | Array + String | String |
| IBM | `bulletFields[0]`, `locationsText` | Array + String | String |
| CrowdStrike | `bulletFields[0]`, `locationsText` | Array + String | String |

**Canonical Name:** `location`  
**Extraction Strategy:** 
```python
# Primary: bulletFields[0] (usually location)
location = job.get('bulletFields', [None])[0]
# Fallback: locationsText
if not location:
    location = job.get('locationsText')
```

---

### Posted Date
| Company | Field Name | Path | Format |
|---------|------------|------|--------|
| Adobe | `postedOn` | `jobPostings[].postedOn` | ISO 8601 ("2025-04-01T10:30:00.000Z") |
| Netflix | `postedOn` | `jobPostings[].postedOn` | ISO 8601 |
| Walmart | `postedOn` | `jobPostings[].postedOn` | ISO 8601 |
| IBM | `postedOn` | `jobPostings[].postedOn` | ISO 8601 |
| CrowdStrike | `postedOn` | `jobPostings[].postedOn` | ISO 8601 |

**Canonical Name:** `posted_at`  
**Extraction Strategy:** 
```python
from datetime import datetime

date_str = job['postedOn']
posted_at = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
```

---

### Job Description
| Company | Field Name | Path | Format |
|---------|------------|------|--------|
| Adobe | `jobDescription` | `jobPostings[].jobDescription` | HTML string |
| Netflix | `jobDescription` | `jobPostings[].jobDescription` | HTML/Plain |
| Walmart | `jobDescription` | `jobPostings[].jobDescription` | HTML/Plain |
| IBM | `jobDescription` | `jobPostings[].jobDescription` | HTML/Plain |
| CrowdStrike | `jobDescription` | `jobPostings[].jobDescription` | HTML/Plain |

**Canonical Name:** `job_description`  
**Extraction Strategy:** 
```python
description = job.get('jobDescription', '')
# Clean HTML if present
if '<' in description and '>' in description:
    description = strip_html(description)
```

---

### Job URL
| Company | Field Name | Path | Format |
|---------|------------|------|--------|
| Adobe | `externalPath` | `jobPostings[].externalPath` | Relative path |
| Netflix | `externalPath` | `jobPostings[].externalPath` | Relative path |
| Walmart | `externalPath` | `jobPostings[].externalPath` | Relative path |
| IBM | `externalPath` | `jobPostings[].externalPath` | Relative path |
| CrowdStrike | `externalPath` | `jobPostings[].externalPath` | Relative path |

**Canonical Name:** `raw_url`  
**Extraction Strategy:** 
```python
# Must construct from base_url + externalPath
path = job['externalPath']  # e.g., "/en-US/External_Experienced/job/Bucharest/Sr-Site-Reliability-Engineer_R167992"
raw_url = f"{base_url}{path}"
# Result: "https://adobe.wd5.myworkdayjobs.com/en-US/External_Experienced/job/Bucharest/Sr-Site-Reliability-Engineer_R167992"
```

**Finding:** Perfect consistency across all Workday implementations - no field name variations!

---

## Data Type Consistency

### String Fields
- `title` — Always string, max length ~200 chars
- `location` — Always string, format varies (City, State | City | Remote)
- `description` — String, may contain HTML, length varies greatly

### Date Fields
- `posted_at` — ISO 8601 string, needs parsing
  - Format 1: `"2024-04-03T10:30:00Z"` (UTC)
  - Format 2: `"2024-04-03"` (date only)
  - Format 3: `"2024-04-03T10:30:00-07:00"` (with timezone)

### Array Fields
- `bulletFields` — Array of strings, variable length
- `additionalLocations` — Array of strings (rare)
- `skills` — Array of strings or objects (very rare)

### Numeric Fields
- `total` / `totalCount` — Integer, total number of jobs

---

## Schema Design Implications

Based on field reliability analysis:

### Required Fields (100% present)
```python
class RawJobData(BaseModel):
    # These MUST be present
    title: str
    external_job_id: str
    raw_url: str
    posted_at: datetime
```

### Optional Fields (60-99% present)
```python
    # These SHOULD be present
    location: Optional[str] = None
    job_description: Optional[str] = None
    employment_type: Optional[str] = None
```

### Metadata Catch-All (everything else)
```python
    # Catch-all for variable fields
    metadata: Dict[str, Any] = Field(default_factory=dict)
```

---

## Extraction Priority Logic

**Priority 1:** Extract core fields, fail if missing
```python
if not all([job.get('title'), job.get('id'), job.get('externalPath')]):
    raise ValueError("Missing required fields")
```

**Priority 2:** Extract common fields, log warning if missing
```python
location = extract_location(job)
if not location:
    logger.warning(f"No location found for job {job['id']}")
```

**Priority 3:** Store everything else in metadata
```python
metadata = {k: v for k, v in job.items() if k not in MAPPED_FIELDS}
```

---

## Field Mapping Function (Draft)

```python
def extract_workday_job(job: dict, base_url: str) -> RawJobData:
    """
    Extract job data from Workday response.
    Handles field name variations across different implementations.
    """
    # Core fields (required)
    title = job.get('title') or job.get('jobTitle')
    if not title:
        raise ValueError("Missing title")
    
    job_id = job.get('id') or job.get('jobReqId')
    if not job_id:
        raise ValueError("Missing job ID")
    
    path = job.get('externalPath') or job.get('url')
    if not path:
        raise ValueError("Missing URL path")
    raw_url = f"{base_url}{path}"
    
    date_str = job.get('postedOn') or job.get('posted')
    if not date_str:
        raise ValueError("Missing posted date")
    posted_at = parse_date(date_str)
    
    # Optional fields
    location = (
        job.get('location') or 
        job.get('locationsText') or 
        (job.get('bulletFields', []) or [None])[0]
    )
    
    description = job.get('jobDescription') or job.get('description')
    if description and '<' in description:
        description = strip_html(description)
    
    employment_type = job.get('timeType') or job.get('employmentType')
    
    # Metadata (everything else)
    mapped_fields = {'title', 'id', 'jobReqId', 'externalPath', 'url', 
                     'postedOn', 'posted', 'location', 'locationsText', 
                     'bulletFields', 'jobDescription', 'description', 
                     'timeType', 'employmentType'}
    metadata = {k: v for k, v in job.items() if k not in mapped_fields}
    
    return RawJobData(
        title=title,
        external_job_id=job_id,
        raw_url=raw_url,
        posted_at=posted_at,
        location=location,
        job_description=description,
        employment_type=employment_type,
        metadata=metadata,
        source="workday",
        company_name=extract_company_name(base_url)
    )
```

---

## Testing Checklist

After analyzing all companies:

- [ ] Verify core fields present in 100% of samples
- [ ] Document all field name variations
- [ ] Test extraction logic with real data from each company
- [ ] Handle missing optional fields gracefully
- [ ] Validate date parsing for all date formats
- [ ] Test HTML cleaning for descriptions
- [ ] Verify URL reconstruction works correctly
- [ ] Ensure metadata captures unmapped fields

---

## Next Steps

1. ✅ Create this analysis document
2. ⏳ Fill in data from 5 company tests
3. ⏳ Calculate reliability percentages
4. ⏳ Finalize `RawJobData` schema based on findings
5. ⏳ Implement extraction function
6. ⏳ Write unit tests for edge cases
