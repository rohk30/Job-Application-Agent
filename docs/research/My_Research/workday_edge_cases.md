# Workday Edge Cases

## Section names vary wildly

NVIDIA

- What you'll be doing
- What we need to see
- Ways to stand out

Samsung

- Position Summary
- Skills and Qualifications

Qualcomm

- General Summary
- Minimum Qualifications
- Preferred Qualifications
- Principal Duties and Responsibilities

Conclusion:

Never rely on section headers.

---

## similarJobs

May be:

```json
[]
```

or

20+ jobs.

Must be optional.

---

## additionalLocations

May not exist.

---

## endDate

Not always present.

---

## remoteType

May not exist.

---

## questionaireId

Optional.

---

## userAuthenticated

Usually false.

Should not be used in filtering.

---

## HTML quality

Job descriptions may contain:

- nested spans
- div soup
- inline styles
- hyperlinks
- malformed HTML

Always clean HTML before LLM processing.