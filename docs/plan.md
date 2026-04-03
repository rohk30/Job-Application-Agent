# 🚀 ApplyMate — Agentic Job Application Copilot

## 🧠 Overview

ApplyMate is an **AI-powered, multi-agent job application system** designed to automate and optimize the end-to-end job application workflow.

Instead of manually searching, tailoring resumes, and tracking applications, ApplyMate:

* Discovers relevant job openings
* Matches them to candidate profiles
* Generates tailored resumes & cover letters
* Assists in application filling (human-in-the-loop)
* Tracks application lifecycle

This system is built using **multi-agent architecture (CrewAI)** combined with a **clean, production-grade backend** following SOLID and clean architecture principles.

---

## 🎯 Problem Statement

Modern job search is:

* Fragmented across multiple portals
* Time-consuming and repetitive
* Highly timing-sensitive
* Poorly tracked by candidates

ApplyMate solves this by acting as an **AI job copilot**.

---

## 🏗️ Architecture Overview

### 🧱 High-Level Architecture

```
Frontend (Web App)
      │
      ▼
Backend API (FastAPI)
      │
      ▼
Application Layer (Orchestrator + Use Cases)
      │
      ▼
Agents (CrewAI)
      │
      ▼
Infrastructure Layer
  ├── PostgreSQL (Core state)
  ├── Vector DB (Embeddings)
  ├── Blob Storage (Resumes)
  ├── Workday Client (Job discovery)
```

---

## 🧠 Core Design Principles

### 1. Clean Architecture

* Domain logic is independent of frameworks
* Infrastructure is replaceable
* Clear separation: Domain → Application → Infra

### 2. SOLID Principles

* Single Responsibility (each agent/service has one role)
* Dependency inversion (interfaces over implementations)
* Open/Closed (easy to extend new portals, agents)

### 3. Agent Design Philosophy

> Agents decide *what* to do.
> Deterministic systems execute *how* to do it.

### 4. Human-in-the-Loop (HIL)

* Authentication and submission always require user control
* No credential exposure to agents

---

## 🤖 Multi-Agent System Design

### 🎯 Orchestrator (Central Controller)

Controls workflow and invokes agents in sequence.

---

### 🔎 Agent 1: Headhunter (Job Discovery)

* Fetches job postings from portals (v1: Workday)
* Filters only active jobs
* Outputs normalized job metadata

---

### 🎯 Agent 2: Strategy Matcher

* Hard filters (eligibility checks)
* Computes match score (0–100)
* Extracts relevant skills & projects

---

### ✍️ Agent 3: Editor

* Tailors resume for job
* Generates cover letter
* Uses only candidate KB (no hallucinations)

---

### 🧭 Agent 4: Application Assistant

* Parses job portal UI
* Prepares form filling plan
* Pauses before submission (HIL)

---

### 📊 Agent 5: Application Tracker

* Maintains lifecycle state machine
* Logs transitions
* Stores application metadata

---

## 🗄️ Database Architecture

### ✅ SQL (PostgreSQL — Source of Truth)

Used for:

* Users
* Candidate profiles
* Resumes (metadata)
* Job postings
* Applications
* Application events (audit log)

### Core Tables

* `users`
* `candidate_profiles`
* `resumes`
* `job_sources`
* `job_postings`
* `applications`
* `application_events`

---

### 🔁 Application State Machine

```
Discovered → Matched → Ready to Apply → Applied
→ Assessment → Interview → Offer / Rejected / Ghosted
```

---

### ⚡ Constraints & Guarantees

* Unique application per (candidate, job)
* Status validation via ENUM-like checks
* Full audit trail via `application_events`
* Indexed for performance

---

### 🧠 NoSQL Components (Planned)

* Vector DB (Qdrant / Weaviate)

  * Resume embeddings
  * Job embeddings

* Blob Storage (S3/MinIO)

  * Resume PDFs
  * Cover letters

---

## 📁 Project Structure

```
backend/
│
├── app/
│   ├── domain/
│   ├── use_cases/
│   ├── agents/
│   ├── repositories/
│   └── services/
│
├── db/
│   ├── models/
│   ├── migrations/
│   ├── base.py
│   └── session.py
│
├── alembic.ini
└── main.py
```

---

## 🔧 Tech Stack

| Layer      | Technology       |
| ---------- | ---------------- |
| Backend    | FastAPI (Python) |
| ORM        | SQLAlchemy       |
| Migrations | Alembic          |
| Database   | PostgreSQL       |
| Vector DB  | Qdrant (planned) |
| Storage    | S3 / MinIO       |
| Agents     | CrewAI           |
| LLM        | OpenAI / Claude  |

---

## 🔐 Security Considerations

* No raw credentials stored
* OAuth-based integrations (future)
* Agents never access sensitive data directly
* Human-in-the-loop for auth & submission
* Audit logging for all state transitions

---

## 🧪 Current Progress (v1 - Phase 1)

### ✅ Completed

* Architecture design (clean + scalable)
* Multi-agent workflow design
* PostgreSQL schema (7 core tables)
* SQLAlchemy + Alembic setup
* Database migrations configured

---

### 🚧 In Progress

* Resume ingestion pipeline
* Workday job discovery client
* Strategy matcher (semantic matching)

---

### ⏳ Upcoming

* Resume tailoring agent
* Application assistant (form parsing)
* Basic frontend dashboard
* Application tracking UI

---

## 🛣️ Roadmap

### 🔹 Phase 1 — Core MVP

* Resume ingestion
* Job discovery (1 portal)
* Matching engine
* Resume + cover letter generation
* Application tracking

---

### 🔹 Phase 2 — Real Integrations

* Gmail integration (status tracking)
* Notifications & reminders
* Multi-portal support

---

### 🔹 Phase 3 — Intelligence Layer

* Interview prep agent
* Skill gap analysis
* Analytics dashboard

---

### 🔹 Phase 4 — Scale & Productization

* OAuth integrations
* Multi-user support
* Rate limiting & infra scaling
* MCP / advanced orchestration

---

## 🧠 Key Design Decisions

### Why SQL for Core State?

* Strong consistency
* Relational queries
* Easier debugging

### Why NoSQL for Embeddings?

* Semantic search
* High-dimensional vector queries

### Why Human-in-the-loop?

* Security
* Compliance
* User trust

### Why Start with Workday?

* Easier scraping
* Less anti-bot friction than LinkedIn

---

## ⚠️ Known Constraints (v1)

* Single job portal
* Limited automation (no auto-submit)
* No email tracking yet
* Manual trigger for workflows

---

## 🔮 Future Vision

ApplyMate evolves into a **Career Operating System**:

* Job discovery
* Application automation
* Interview preparation
* Offer optimization
* Long-term career tracking

---

## 🏁 Final Philosophy

> Build systems that are:

* Observable
* Modular
* Secure
* Extensible

And most importantly:

> Solve a real problem, not just showcase AI.

---

## 👨‍💻 Author Notes

This project is designed to:

* Demonstrate real-world agentic AI systems
* Showcase production-ready backend architecture
* Solve a high-impact user problem

---
