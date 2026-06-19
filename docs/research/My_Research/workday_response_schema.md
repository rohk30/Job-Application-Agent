# Workday Response Schema

## Search endpoint

Returns

```json
{
  "total": 172,
  "jobPostings": []
}
```

---

## JobPostingSummary

```python
title
externalPath
locationsText
postedOn
remoteType (optional)
bulletFields
```

---

## Job details endpoint

Returns

```json
{
  "jobPostingInfo": {},
  "hiringOrganization": {},
  "similarJobs": [],
  "userAuthenticated": false
}
```

---

## jobPostingInfo

Contains:

```python
id
title
jobDescription
location
additionalLocations
postedOn
startDate
timeType
jobReqId
jobPostingId
jobPostingSiteId
country
canApply
posted
includeResumeParsing
jobRequisitionLocation
remoteType
externalUrl
questionnaireId
timeLeftToApply
endDate
jobPostingEndDateAsText
```