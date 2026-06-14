# 🏗️ ApplyMate — System Architecture

## 🧱 Architecture Style

Clean Architecture (Hexagonal)

```
Domain → Application → Infrastructure
```

---

## 📦 Layer Breakdown

### 1. Domain Layer

* Entities (User, Job, Application)
* Value objects
* Repository interfaces

No external dependencies.

---

### 2. Application Layer

* Use cases
* Orchestrator
* Agent coordination

Controls system flow.

---

### 3. Infrastructure Layer

* Database (Postgres)
* Vector DB
* LLM APIs
* Portal clients
* Storage

Implements interfaces.

---

## 🔁 Core Workflow

```
Headhunter → Strategy Matcher → Editor → Assistant → Tracker
```

---

## 🤖 Agent Architecture

### Orchestrator

* Controls execution flow
* Invokes agents sequentially

---

### Worker Agents

* Stateless
* Single responsibility
* JSON input/output contracts

---

## 🗄️ Data Flow

```
Portal → Headhunter → DB (jobs)
        ↓
Strategy Matcher → DB (applications)
        ↓
Editor → Storage (resume/cover letter)
        ↓
Assistant → UI (HIL)
        ↓
Tracker → DB (state + events)
```

---

## 🧩 Module Structure

```
app/
  domain/
  use_cases/
  agents/
  repositories/
  services/

db/
  models/
  migrations/
```

---

## 🔌 External Systems

* Workday (job source)
* LLM API
* Vector DB
* Storage

---

## 🔐 Security Architecture

* No credential access by agents
* HIL for sensitive operations
* Minimal data exposure to LLMs

---

## ⚡ Scalability Design

* Stateless agents
* Async job processing
* Background workers (future)
* Horizontal scaling possible

---

## 🔍 Observability (Future)

* Agent logs
* Execution traces
* Cost tracking
* Failure analysis

---

## 🔮 Extensibility

Future additions:

* Multi-portal support
* Email integration
* Interview prep agent
* Analytics engine

---

## 🧠 Architectural Principles

1. Separation of concerns
2. Dependency inversion
3. Stateless agents
4. Deterministic core logic
5. Event-driven tracking

---

## 🏁 Summary

This system is designed to:

* Scale from MVP → production
* Remain debuggable under complexity
* Balance AI flexibility with system reliability
