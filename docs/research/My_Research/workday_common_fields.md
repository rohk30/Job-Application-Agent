# Common Workday Fields

## Mandatory fields observed across companies

```python
title
jobDescription
location
postedOn
startDate
timeType
jobReqId
jobPostingId
jobPostingSiteId
country
canApply
posted
externalUrl
```

---

## Frequently observed

```python
additionalLocations
remoteType
questionnaireId
timeLeftToApply
endDate
jobPostingEndDateAsText
```

---

## Nested structures

### country

```json
{
  "descriptor": "India",
  "id": "...",
  "alpha2Code": "IN"
}
```

---

### jobRequisitionLocation

```json
{
  "descriptor": "India, Bengaluru",
  "country": {}
}
```

---

### hiringOrganization

```json
{
  "name": "...",
  "url": ""
}
```

---

### similarJobs

```json
[
{
"title":"",
"externalPath":"",
"timeType":"",
"locationsText":"",
"postedOn":"",
"startDate":""
}
]
```

---

## Recommended DTO split

Core DTO:

```python
RawJobData
```

Optional fields:

```python
metadata: dict[str, Any]
```

to avoid schema explosion.