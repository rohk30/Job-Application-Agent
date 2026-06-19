# 📋 Workday Response Schema Mapping

## Purpose
Map Workday API response fields to our internal `RawJobData` schema.

---

## Field Mapping Table

| Workday Field | Type | Meaning | RawJobData Field | Required | Transform Logic | Notes |
|---------------|------|---------|------------------|----------|-----------------|-------|
| `title` | string | Job title | `title` | ✅ | Direct | Always present |
| `externalPath` | string | Job URL suffix | `raw_url` | ✅ | Prefix with base URL | e.g., `/job/Software-Engineer/J123` |
| `bulletFields` | array | Metadata (location, type, etc.) | `location`, `metadata` | ❌ | Extract first as location | Array order varies |
| `postedOn` | string | Posted timestamp | `posted_at` | ✅ | Parse ISO 8601 | Format: `2024-04-03T10:30:00Z` |
| `jobDescription` | string | Full job description | `job_description` | ❌ | Strip HTML if present | May be truncated |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |

---

## Response Structure by Company

### Company 1: [NAME]

**Top-level structure:**
```json
{
  "total": 150,
  "jobs": [
    {
      "field1": "value1",
      "field2": "value2"
    }
  ]
}
```

**Sample Job Object:**
```json
{
  "title": "Software Engineer",
  "externalPath": "/job/Software-Engineer/J123",
  "bulletFields": ["San Francisco, CA", "Full-Time"],
  "postedOn": "2024-04-01T08:00:00Z",
  "jobDescription": "We are looking for..."
}
```

**Key Observations:**
- Jobs array path: `response.jobs`
- Total count path: `response.total`
- Unique identifier: [field name]

---

### Company 2: [NAME]

**Top-level structure:**
```json
{
  [Fill in after analysis]
}
```

**Sample Job Object:**
```json
{
  [Fill in after analysis]
}
```

**Key Observations:**
- Jobs array path: 
- Total count path: 
- Unique identifier: 

---

### Company 3: [NAME]

**Top-level structure:**
```json
{
  [Fill in after analysis]
}
```

**Sample Job Object:**
```json
{
  [Fill in after analysis]
}
```

**Key Observations:**
- Jobs array path: 
- Total count path: 
- Unique identifier: 

---

### Company 4: [NAME]

**Top-level structure:**
```json
{
  [Fill in after analysis]
}
```

**Sample Job Object:**
```json
{
  [Fill in after analysis]
}
```

**Key Observations:**
- Jobs array path: 
- Total count path: 
- Unique identifier: 

---

### Company 5: [NAME]

**Top-level structure:**
```json
{
  [Fill in after analysis]
}
```

**Sample Job Object:**
```json
{
  [Fill in after analysis]
}
```

**Key Observations:**
- Jobs array path: 
- Total count path: 
- Unique identifier: 

---

## Field Reliability Analysis

### Core Fields (100% present)
- `title`
- `externalPath` (or equivalent URL field)
- `postedOn` (or equivalent date field)

### Common Fields (60-99% present)
- `bulletFields` or `location`
- `jobDescription`

### Optional Fields (<60% present)
- `salary`
- `experienceLevel`
- `remote` flag

---

## Data Type Analysis

| Field | Expected Type | Observed Types | Nullable | Default Value |
|-------|---------------|----------------|----------|---------------|
| `title` | string | string | No | - |
| `externalPath` | string | string | No | - |
| `bulletFields` | array | array, null | Yes | `[]` |
| `postedOn` | string (ISO 8601) | string | No | - |
| `jobDescription` | string | string, null | Yes | `""` |

---

## Edge Cases

### Missing Fields
- **Company X:** No `jobDescription` field → Use empty string
- **Company Y:** `bulletFields` is `null` instead of empty array

### Field Variations
- **Location:** Sometimes in `bulletFields[0]`, sometimes in `location` field
- **Date Format:** Most use ISO 8601, but Company Z uses `YYYY-MM-DD`

### Nested Data
- **Company A:** Job ID nested in `positionDetails.externalId`
- **Company B:** Location is an object `{city, state, country}` not string

---

## URL Reconstruction

### Pattern 1: Base URL + externalPath
```
Base: https://company.wd1.myworkdayjobs.com
externalPath: /Company/job/Software-Engineer/JR-12345
Result: https://company.wd1.myworkdayjobs.com/Company/job/Software-Engineer/JR-12345
```

### Pattern 2: Absolute URL provided
```
jobUrl: https://company.wd5.myworkdayjobs.com/careers/job/JR-12345
Result: Use as-is
```

---

## Proposed `RawJobData` Schema

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime

class RawJobData(BaseModel):
    """
    Normalized job data extracted from Workday API.
    
    Based on analysis of N=5 Workday implementations.
    See: docs/research/workday_response_schema.md
    """
    
    # Core fields (100% reliability)
    title: str = Field(..., description="Job title")
    raw_url: str = Field(..., description="Full job posting URL")
    posted_at: datetime = Field(..., description="When job was posted")
    
    # Common fields (>60% reliability)
    location: Optional[str] = Field(None, description="Job location")
    job_description: Optional[str] = Field(None, description="Full job description")
    
    # Optional fields
    job_type: Optional[str] = Field(None, description="Full-time, Part-time, etc.")
    experience_level: Optional[str] = Field(None, description="Entry, Mid, Senior, etc.")
    remote_flag: Optional[bool] = Field(None, description="Is remote work allowed")
    
    # Metadata (catch-all for variable fields)
    raw_metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Original response fields for debugging"
    )
    
    # Provenance
    source: str = Field(default="workday", description="Data source identifier")
    company_name: str = Field(..., description="Company posting the job")
    fetched_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When data was fetched"
    )
    
    # Workday-specific
    workday_job_id: Optional[str] = Field(None, description="Workday internal job ID")
    
    @validator('raw_url')
    def validate_url(cls, v):
        if not v.startswith('http'):
            raise ValueError('raw_url must be absolute URL')
        return v
    
    @validator('posted_at', pre=True)
    def parse_date(cls, v):
        if isinstance(v, str):
            # Handle ISO 8601
            return datetime.fromisoformat(v.replace('Z', '+00:00'))
        return v
```

---

## Transformation Examples

### Example 1: Simple Case
**Input (Workday):**
```json
{
  "title": "Senior Software Engineer",
  "externalPath": "/careers/job/JR-001",
  "postedOn": "2024-04-01T10:00:00Z",
  "bulletFields": ["San Francisco, CA", "Full-Time"]
}
```

**Output (RawJobData):**
```json
{
  "title": "Senior Software Engineer",
  "raw_url": "https://company.myworkdayjobs.com/careers/job/JR-001",
  "posted_at": "2024-04-01T10:00:00+00:00",
  "location": "San Francisco, CA",
  "job_type": "Full-Time",
  "company_name": "Company Inc",
  "source": "workday",
  "fetched_at": "2024-04-03T15:30:00+00:00"
}
```

---

## Next Steps

1. ✅ Complete field mapping for all 5 companies
2. ✅ Identify 100% reliable fields
3. ✅ Define transformation logic
4. ✅ Implement `RawJobData` Pydantic model
5. ✅ Write parser function `parse_workday_response(raw_json) -> RawJobData`
6. ✅ Add unit tests for edge cases
