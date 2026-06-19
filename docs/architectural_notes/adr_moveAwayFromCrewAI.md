# ADR-001: Framework and Orchestration Strategy

## Status

Accepted

---

# Context

ApplyMate was initially conceived as a multi-agent system built around CrewAI.

The early architectural assumption was:

```text
User
↓
CrewAI Agents
↓
Tools
↓
Database
```

CrewAI was chosen primarily because:

* Familiarity and ease of learning.
* Good developer experience.
* Rapid prototyping capabilities.
* Strong conceptual alignment with "multi-agent systems".

As the project matured and moved from prototype-level thinking toward production-grade architecture, the requirements of the system became clearer.

---

# Observations

ApplyMate is fundamentally a:

> Stateful workflow orchestration problem.

rather than a:

> Autonomous multi-agent collaboration problem.

The lifecycle of an application spans weeks or months:

```text
Discovered
↓
Matched
↓
Tailored
↓
Applied
↓
Assessment
↓
Interview
↓
Offer / Reject
```

This introduces requirements that are workflow-centric rather than agent-centric:

* Persistent execution
* Interruptibility
* Human-in-the-loop checkpoints
* Retryability
* State transitions
* Long-running processes
* Observability
* Event sourcing
* Background execution

---

# Problem With Pure Multi-Agent Frameworks

Frameworks such as CrewAI optimize for:

* Agent collaboration
* Role delegation
* Short-lived workflows
* Rapid prototyping

However, they provide weaker support for:

* Long-lived state
* Persistence
* Recovery
* Human approvals
* Event-driven workflows
* Deterministic execution

Over time, forcing the product architecture to follow the framework architecture could lead to:

* Agent spaghetti
* Hidden state
* Difficult debugging
* Poor observability
* Major rewrites

---

# Architectural Principle

The project should never become:

```text
ApplyMate
↓
CrewAI Architecture
```

or

```text
ApplyMate
↓
LangGraph Architecture
```

Instead:

```text
ApplyMate
↓
Domain Model
↓
Application Services
↓
Repositories
↓
Workflow Layer
↓
Reasoning Layer
↓
Infrastructure
```

Frameworks must remain replaceable infrastructure components.

---

# Decision

The project will move away from a CrewAI-centric architecture.

ApplyMate will instead be designed as:

> A stateful workflow system with specialized reasoning nodes.

---

# Selected Direction

Primary orchestration framework:

## LangGraph

Reasoning layer:

## PydanticAI

Storage:

## PostgreSQL + pgvector

API Layer:

## FastAPI

Persistence:

## SQLAlchemy + Alembic

---

# Updated Philosophy

Previous philosophy:

```text
Multiple agents collaborating
```

New philosophy:

```text
State machine
↓
Workflow nodes
↓
Reasoning where necessary
↓
Deterministic execution elsewhere
```

---

# Architectural Layers

## Domain Layer

Contains:

* Entities
* Value objects
* Business rules
* Repository interfaces

No framework dependencies.

---

## Application Layer

Contains:

* Use cases
* Services
* Orchestrators

Responsible for business flow.

---

## Workflow Layer

Implemented using LangGraph.

Responsible for:

* State transitions
* Human approvals
* Retries
* Interruptions
* Persistence

---

## Reasoning Layer

Implemented using PydanticAI.

Responsible for:

* Matching
* Resume tailoring
* Keyword extraction
* Interview preparation

Reasoning components are stateless and structured.

---

## Infrastructure Layer

Contains:

* PostgreSQL
* pgvector
* LLM providers
* Workday client
* Email integrations
* Storage systems

---

# High-Level Future Architecture

```text
FastAPI
↓
Application Services
↓
Repositories
↓
LangGraph Workflow Engine
↓
PydanticAI Reasoning Nodes
↓
LLMs
↓
PostgreSQL + pgvector
```

---

# Workflow Philosophy

Most nodes should remain deterministic.

LLMs should only be introduced where semantic reasoning is genuinely required.

Examples:

### Deterministic

* Job discovery
* State transitions
* Event logging
* Application tracking

### LLM-Assisted

* Match scoring
* Resume editing
* Cover letter generation
* Interview preparation

---

# Human-in-the-Loop

Human approval nodes are first-class concepts.

Examples:

```text
Prepare Application
↓
Human Approval
↓
Submit
```

and

```text
Interview Invitation
↓
Human Confirmation
↓
Interview Preparation
```

The system should never attempt to bypass:

* Authentication
* CAPTCHA
* Platform security boundaries

---

# Evolution Plan

## Phase 1

No orchestration framework.

Build:

* Services
* Repositories
* Use cases

Framework-independent.

---

## Phase 2

Introduce LangGraph.

Convert use cases into workflow nodes.

Examples:

```text
discover_jobs()

match_jobs()

generate_resume()

track_application()
```

---

## Phase 3

Add:

```text
Discover
↓
Match
↓
Edit
↓
Apply
↓
Track
```

workflow graph.

---

## Phase 4

Introduce:

* Human approval nodes
* Email monitoring
* Interview preparation

---

## Phase 5

Introduce:

* Multi-user workflows
* Background execution
* Long-lived sessions

---

## Future Considerations

Temporal may eventually be introduced if:

* Workflows become month-long.
* Reliability requirements increase.
* Distributed execution becomes necessary.

---

# Consequences

## Advantages

* Better observability.
* Easier debugging.
* Strong persistence.
* Cleaner architecture.
* Framework independence.
* Easier scaling.
* More production-ready.

---

## Tradeoffs

* Increased complexity.
* Steeper learning curve.
* More verbose implementation.
* Slower initial development.

---

# Guiding Principle

> ApplyMate is not a multi-agent project.

It is a career intelligence platform implemented as a stateful workflow system with specialized reasoning nodes.

Frameworks are infrastructure.

The domain model remains the center of the architecture.
