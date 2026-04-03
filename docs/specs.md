# 📘 ApplyMate — Product & System Specifications

## 🎯 Product Goal

Build an AI-powered system that:

* Discovers job opportunities
* Matches them to candidates
* Generates tailored applications
* Assists submission (HIL)
* Tracks application lifecycle

---

## 👤 Actors

### Primary User

* Job-seeking candidate

### System Actors

* Orchestrator
* Agents (Discovery, Matching, Editor, Assistant, Tracker)
* Backend services
* External systems (job portals, email, storage)

---

## 🧾 Functional Requirements

### 1. Candidate Profile Management

* Upload resumes (PDF)
* Store structured candidate data
* Maintain multiple profiles (future)

---

### 2. Job Discovery

* Fetch jobs from supported portals (v1: Workday)
* Validate job is active
* Store normalized job metadata

---

### 3. Job Matching

* Hard filters:

  * Experience level
  * Location
  * Role mismatch
* Compute match score (0–100)
* Extract relevant skills/projects

---

### 4. Resume Tailoring

* Generate role-specific resume
* Generate cover letter
* Maintain versioning

---

### 5. Application Assistance

* Parse job application page
* Generate field-fill plan
* Pause for user verification before submission

---

### 6. Application Tracking

* Maintain lifecycle states
* Log all state transitions
* Track timestamps and metadata

---

## 🔁 Application Lifecycle

```
discovered → matched → ready_to_apply → applied
→ assessment → interview → offer / rejected / ghosted
```

---

## 📊 Non-Functional Requirements

### Performance

* Job discovery must be async
* Matching should support batching
* LLM calls should be minimized and cached

---

### Scalability

* Support multiple job portals
* Support multiple candidates per user
* Horizontal scaling of workers

---

### Reliability

* Idempotent operations
* Retry-safe workflows
* Audit logs for all transitions

---

### Security

* No credential storage
* Human-in-the-loop for auth
* Encrypted sensitive data

---

## 🧠 Data Requirements

### Structured Data (SQL)

* Users
* Candidates
* Jobs
* Applications
* Events

### Unstructured Data

* Resume PDFs
* Job descriptions
* Cover letters

### Semantic Data (Vector DB)

* Resume embeddings
* Job embeddings

---

## 🔌 External Integrations

* Job portals (Workday v1)
* Gmail API (future)
* Storage (S3/MinIO)
* LLM providers

---

## 🧪 MVP Scope

### Included

* 1 job portal (Workday)
* 3 candidate profiles
* Matching + scoring
* Resume + cover letter generation
* Application tracking

### Excluded

* Auto submission
* Email monitoring
* Multi-portal support
* Interview preparation

---

## 📌 Success Metrics (Future)

* Match accuracy
* Application → interview conversion rate
* Time saved per user
* Resume performance metrics
