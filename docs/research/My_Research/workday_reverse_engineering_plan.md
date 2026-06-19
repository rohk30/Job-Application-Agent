# Reverse Engineering Journey

## Phase 1

Hypothesis:

Each company might need its own provider.

Example:

```python
NvidiaProvider
AdobeProvider
SamsungProvider
```

---

## Phase 2

Observed:

Search endpoint schemas identical.

---

## Phase 3

Observed:

Detail endpoint schemas identical.

---

## Phase 4

Observed:

Tenants (wd3, wd5, wd12) do not affect payloads.

---

## Phase 5

Conclusion

Provider becomes:

```python
WorkdaySearchProvider
```

instead of company-specific providers.

---

## Phase 6

Original parser design

```text
RawJobData
↓
JobPageParser
↓
ParsedJobData
```

---

## Phase 7

New architecture

```text
RawJobData
↓
HtmlCleaner
↓
PlainJobDocument
↓
LLMJobUnderstandingService
↓
EnrichedJobData
↓
JobValidator
↓
Repository
```

---

Reason:

Semantic meaning is stable.

Section names are not.

LLMs are better suited for understanding responsibilities, skills, education, YOE and keywords.