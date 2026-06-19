# Workday Reverse Engineering – Sample Companies

## Objective

Verify whether Workday career sites expose a common API schema across companies and tenants.

---

# NVIDIA

Tenant:

```
wd5
```

Career site:

```
https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite
```

### Search endpoint

POST

```
/wday/cxs/nvidia/NVIDIAExternalCareerSite/jobs
```

Response:

```json
{
  "total": 172,
  "jobPostings": [
    {
      "title": "Cyber Security Analyst",
      "externalPath": "/job/India-Bengaluru/Cyber-Security-Analyst_JR2015853",
      "locationsText": "2 Locations",
      "postedOn": "Posted 2 Days Ago",
      "bulletFields": ["JR2015853"]
    }
  ]
}
```

### Job details endpoint

Returns:

```json
{
  "jobPostingInfo": {},
  "hiringOrganization": {},
  "similarJobs": [],
  "userAuthenticated": false
}
```

Interesting observations:

- additionalLocations exists
- similarJobs empty
- canApply = true
- includeResumeParsing = true

---

# Salesforce

Tenant

```
wd12
```

Interesting fields:

```json
{
  "remoteType": "Office - Flexible",
  "timeLeftToApply": "3 days left to apply",
  "endDate": "2026-06-23",
  "jobPostingEndDateAsText": "End Date: June 23, 2026"
}
```

New discoveries:

- application deadlines
- urgency metadata
- remote work type

---

# Adobe

Tenant

```
wd5
```

Interesting findings:

similarJobs populated heavily.

Example:

```json
"similarJobs":[
{
"title":"Principal Applied Researcher"
},
{
"title":"Senior Machine Learning Engineer"
}
]
```

Architectural implication:

Job graph expansion is possible.

---

# Samsung

Tenant

```
wd3
```

Interesting findings:

Search response exposes facets.

Example:

```json
{
  "facetParameter":"remoteType"
}
```

Other facet types:

- Country
- Hiring Company
- Job Category
- Job Type
- Time Type
- Locations

Architectural implication:

Filters can be discovered dynamically.

---

# Qualcomm

Tenant

```
wd12
```

Interesting findings:

Large populated similarJobs list.

Section names differ:

- General Summary
- Minimum Qualifications
- Preferred Qualifications
- Principal Duties and Responsibilities

This confirms that deterministic section extraction is unreliable.

---

# Conclusion

Different companies:

- NVIDIA
- Salesforce
- Adobe
- Samsung
- Qualcomm

Different tenants:

- wd3
- wd5
- wd12

Yet all expose nearly identical response schemas.

Conclusion:

Workday protocol is standardized.

Providers should be implemented at the Workday level, NOT company level.