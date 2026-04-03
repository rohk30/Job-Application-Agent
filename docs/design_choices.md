# 🧠 ApplyMate — Design Choices & Rationale

## 🎯 Philosophy

The system is designed to:

* Prioritize correctness over automation
* Be modular and extensible
* Avoid “agent spaghetti”
* Maintain strict control over side effects

---

## 🤖 Multi-Agent Design

### Choice: Hierarchical Agent Architecture

Instead of:

* Fully autonomous agents
* Peer-to-peer communication

We use:

* Central orchestrator
* Specialized worker agents

### Why:

* Easier debugging
* Better observability
* Controlled execution
* Lower cost

---

## 🧠 LLM Usage Strategy

### Choice: LLM for reasoning only

LLM is used for:

* Semantic matching
* Keyword extraction
* Content generation

LLM is NOT used for:

* State transitions
* DB operations
* Critical logic

### Why:

* Determinism
* Reliability
* Security

---

## 🗄️ Database Strategy

### Choice: SQL (Postgres) for core state

Why:

* Strong consistency
* Relational queries
* Transaction safety
* Easier debugging

---

### Choice: NoSQL for embeddings & files

* Vector DB → semantic search
* Blob storage → documents

Why:

* Scalability
* Cost efficiency
* Performance

---

## 🔐 Authentication Design

### Choice: Human-in-the-loop

System:

* Does not store credentials
* Does not bypass auth systems

Why:

* Security
* Compliance
* Trust

---

## 🌐 Portal Strategy

### Choice: Start with Workday

Why:

* Structured pages
* Easier parsing
* Lower anti-bot complexity

Avoided:

* LinkedIn (initially)

---

## 🧩 Application Assistant Design

### Choice: Plan → Execute separation

Agent:

* Generates fill plan

Backend:

* Executes actions

Why:

* Prevent hallucinated actions
* Improve reliability
* Easier debugging

---

## 📊 Tracking System Design

### Choice: Event-driven tracking

* applications table = current state
* application_events = history

Why:

* Full audit trail
* Debuggable
* Extensible

---

## 🔁 Resume System Design

### Choice: Versioned resumes

* Each job gets tailored version
* Stored separately

Why:

* Traceability
* Performance analysis
* A/B testing potential

---

## ⚠️ Tradeoffs

| Decision                  | Tradeoff        |
| ------------------------- | --------------- |
| HIL instead of automation | Slower UX       |
| SQL over NoSQL            | Slight rigidity |
| Controlled agents         | Less “autonomy” |
| Workday over LinkedIn     | Less coverage   |

---

## 🧠 Guiding Principle

> Build a system that is:

* Predictable
* Inspectable
* Extendable

Not just “intelligent”.
