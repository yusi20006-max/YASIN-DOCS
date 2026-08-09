# YASIN Ecosystem — Canonical Architecture v1

> Canonical architecture baseline for the Yasin ecosystem. This document is intended to give a new engineer or AI agent enough context to understand project roles, ownership, boundaries, dependencies, operational control, and integration rules before modifying code.

- Status: Canonical Draft v1
- Date: 2026-08-10
- Evidence policy: confirmed source-level relationships are distinguished from inferred and future relationships.

## 1. Executive Summary

Yasin is a multi-project ecosystem, not a monolithic application. Its current architecture separates five major concerns:

1. **Core runtime** — Yasin-Core provides generic runtime and SDK foundations.
2. **Agent execution** — Yasin-Agent provides agent/workflow execution on top of Core.
3. **AI platform** — Yasin-AI provides AI runtime, knowledge, durable memory, API/service, extensions, and observability capabilities.
4. **Control/operations** — YasinHub provides ecosystem lifecycle control, status, health, and operational integration.
5. **Unified user interface** — YasinCLI provides the user-facing command surface and ecosystem orchestration.

Content applications form another family:

- YasinRelay — Telegram/content relay and publishing pipeline.
- YasinFeed — general content aggregation/processing/publishing platform.
- YasinPress — specialized Persian-news publishing automation.

These projects share ecosystem operations but do not automatically share business logic, storage, or AI infrastructure.

## 2. Canonical Layer Model

```text
USER / OPERATOR
       │
       ▼
┌──────────────────────────────┐
│          YasinCLI            │
│ Unified UX / Commands        │
│ Ecosystem Orchestration      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          YasinHub            │
│ Control Plane                │
│ Observability / Lifecycle    │
└───────┬────────┬────────┬────┘
        │        │        │
        ▼        ▼        ▼
      Core     Agent    Applications
                         │
                   ┌─────┼──────────┐
                   ▼     ▼          ▼
                 Relay  Feed      Press

              Yasin-AI
      ┌──────────┼──────────┐
      ▼          ▼          ▼
  Knowledge    Memory    API/Runtime
```

Yasin-AI is currently an independent platform boundary. A direct AI → Core dependency is **not established** by the audit evidence and must not be invented.

## 3. Project Responsibility Matrix

| Project | Primary responsibility | Operationally controlled by | Confirmed direct dependencies |
|---|---|---|---|
| Yasin-Core | Generic runtime + SDK foundation | Hub / CLI | — |
| Yasin-Agent | Agent/workflow execution | Hub / CLI | Yasin-Core |
| Yasin-AI | AI runtime, knowledge, memory, API, extensions, observability | Ecosystem operations | Direct Core edge not established |
| YasinHub | Control + observability + lifecycle operations | Operator / CLI | Core SDK, Agent SDK |
| YasinCLI | Unified UX + ecosystem orchestration | Operator | Core/Agent/Hub/Relay adapters |
| YasinRelay | Telegram/content processing/publishing | Hub / CLI | AIProcessor abstraction |
| YasinFeed | General content aggregation/processing/publishing | Hub / CLI | Provider adapters |
| YasinPress | Specialized Persian news automation | Hub / CLI | Optional Cloudflare AI integration |

## 4. Confirmed Dependency Graph

```text
Yasin-Agent ───────────────→ Yasin-Core

YasinHub ──────────────────→ Yasin-Core SDK
YasinHub ──────────────────→ Yasin-Agent SDK

YasinCLI ──────────────────→ ecosystem adapters
                              ├─ Core
                              ├─ Agent
                              ├─ Hub
                              └─ Relay
```

Operational relationship:

```text
Operator → YasinCLI → YasinHub → {Core, Agent, Relay, Feed, Press, AI, ...}
```

Operational control does not mean every project imports Hub.

## 5. Explicitly Unconfirmed Relationships

Until source evidence and an explicit contract exist, do not document these as dependencies:

```text
Yasin-AI → Yasin-Core
Yasin-Relay → Yasin-AI
Yasin-Feed → Yasin-AI
Yasin-Press → Yasin-AI
Shared ecosystem database → all applications
Global event bus → all applications
```

## 6. Yasin-Core

### Mission

Provide reusable runtime and SDK foundations for the ecosystem.

### Boundary

Core is a foundation layer. Higher-level application concerns must not be pushed into Core merely for convenience.

```text
Core → runtime / SDK foundations
Core ✕ Hub internals
Core ✕ Press business logic
Core ✕ Feed business logic
Core ✕ Relay business logic
```

## 7. Yasin-Agent

### Mission

Provide agent and workflow execution capabilities.

### Core relationship

The audit confirms Agent → Core. Agent is therefore a runtime/application layer built on the generic Core foundation.

```text
Yasin-Agent
     ↓
Yasin-Core
```

Agent should expose stable public contracts to higher-level tooling rather than require Hub internals.

## 8. Yasin-AI

### Mission

Provide an AI platform containing:

- runtime/module orchestration;
- knowledge retrieval, embeddings, and graph/reasoning primitives;
- durable memory and storage;
- developer/plugin extension contracts;
- transport-neutral API/service layer;
- observability primitives;
- deployment configuration.

### Persistence

SQLite is the default local persistence mechanism for memory and semantic indexes. This is platform-owned durable state and is distinct from application-local state in Feed, Press, or Relay.

### Plugin security

Current plugin execution is trusted/in-process. Remote untrusted execution is not established as supported; sandboxing and authorization remain future security concerns.

### Version note

The audited repository showed a README production-release/package-version mismatch. This is a release-management issue and should be resolved independently of ecosystem architecture.

## 9. YasinHub

### Mission

YasinHub is the ecosystem **control and observability plane**.

### Responsibilities

- status aggregation;
- process and health detection;
- lifecycle commands;
- Core SDK integration;
- Agent SDK integration;
- Relay operational controls;
- ecosystem registry;
- dashboard/doctor-style operator visibility.

### Boundary

Hub controls other projects but does not own their internal business logic.

```text
Hub
 ↓ public SDK/API/process contract
Project runtime
```

A project should remain capable of executing its core business logic without importing Hub internals.

## 10. YasinCLI

### Mission

Provide a unified user-facing command surface across the ecosystem.

### Architectural role

YasinCLI is not a second implementation of each project's internals. It uses adapters and orchestration and delegates project-specific behavior to the appropriate boundary.

### Relationship with Hub

Hub already has a central control CLI. Therefore YasinCLI must not become a competing implementation of Hub's operational logic.

Recommended hierarchy:

```text
User
 ↓
YasinCLI
 ↓
Public SDK / API / Adapter
 ↓
YasinHub
 ↓
Project runtimes
```

The current audit identified first-class adapters for Core, Agent, Hub, and Relay. Feed, Press, and AI should be treated as future adapter work until explicitly implemented.

## 11. YasinRelay

### Mission

Content ingestion, transformation, and publication pipeline with current Telegram → Eitaa orientation.

### Pipeline

```text
Telegram → Collector → Normalizer → Validator → Duplicate Detection
          → AIProcessor → Media Processor → Publisher → Eitaa
```

### AI boundary

Relay owns an `AIProcessor` abstraction. Providers can be replaced without rewriting the pipeline. This abstraction is deliberately separate from Yasin-AI until an explicit integration contract is designed.

### Storage

Relay SQLite is operational pipeline state, not ecosystem-wide memory.

### Events

Relay events are currently internal pipeline events, not a confirmed global ecosystem event bus.

## 12. YasinFeed

### Mission

General-purpose content aggregation, processing, storage, rewriting, and publishing.

### Outputs

- RSS;
- PWA/API JSON;
- Eitaa.

Feed owns its application pipeline; ecosystem lifecycle is externalized to Hub/CLI.

Feed has provider-specific AI/rewrite extension points. These remain adapters until a deliberate shared AI contract exists.

## 13. YasinPress

### Mission

Specialized Persian-news publishing automation, primarily for Eitaa.

### Pipeline

```text
RSS → Collection → Duplicate Detection → Age/Priority/Category
    → Optional Cloudflare Workers AI → Builder/Formatter/Tags
    → Durable Queue → Rate Limiter → Eitaa
```

### Relationship to Feed

Feed and Press overlap in RSS/news functionality but currently represent distinct product boundaries. A future shared content-platform layer is an architectural opportunity, not a current dependency.

## 14. Storage Architecture

There is intentionally no confirmed shared application database.

```text
Yasin-AI    → durable platform memory / semantic indexes
YasinRelay  → pipeline-state SQLite
YasinFeed   → application storage
YasinPress  → application-state SQLite
```

A shared datastore requires an explicit ADR and contract. It must not arise through accidental filesystem/database coupling.

## 15. AI Provider Architecture

Current capability is distributed:

```text
YasinRelay → AIProcessor
YasinFeed  → provider adapters
YasinPress → optional Cloudflare Workers AI
Yasin-AI   → AI platform
```

Do not collapse these into a single provider architecture until a shared contract is deliberately designed.

## 16. Event Architecture

Current confirmed scopes:

```text
Relay internal events → local pipeline scope
Hub status contract   → ecosystem operational scope
Project SDK/API       → explicit control scope
```

There is no confirmed global event bus. A future bus requires schema/versioning, delivery semantics, retries, idempotency, security, ownership, and an ADR.

## 17. Security Boundaries

Security responsibilities remain local to each boundary:

- Core: runtime security contracts;
- Agent: execution/tool security;
- AI: plugin trust, API/service security, memory access;
- Hub: operator/control authorization;
- CLI: local credential/config handling;
- Feed/Press/Relay: provider credentials and publishing permissions.

No project should assume another project's internal security model is automatically inherited.

## 18. Lifecycle Model

```text
YasinCLI
   ↓
YasinHub
   ↓
start / stop / restart / health / doctor
   ↓
Project-specific runtime
```

The project owns execution semantics; Hub owns ecosystem-level operational coordination.

## 19. Dependency Direction Rules

### Allowed

```text
Application → public platform SDK
Hub → public project SDK
CLI → adapters / public APIs
Agent → Core
```

### Discouraged / prohibited without explicit approval

```text
Core → Hub
Core → Press/Feed/Relay
Agent → Hub internals
Project → Hub internal modules
Shared database → implicit cross-project coupling
```

## 20. Canonical Terms

| Term | Meaning |
|---|---|
| Runtime Plane | Execution logic of an individual project |
| Control Plane | Ecosystem lifecycle and operational coordination |
| Observability Plane | Status, health, metrics, and diagnostics |
| Platform | Reusable capability boundary such as Core or AI |
| Application | Product-specific pipeline such as Feed, Press, or Relay |
| Adapter | Integration boundary around another service/provider |
| Operational State | Local state required to run a project |
| Ecosystem Memory | Shared durable memory only if explicitly introduced |

## 21. Current Canonical Graph

```text
                              USER
                               │
                               ▼
                         ┌───────────┐
                         │ YasinCLI  │
                         └─────┬─────┘
                               │
                               ▼
                         ┌───────────┐
                         │ YasinHub  │
                         │ Control + │
                         │ Observe   │
                         └─┬──┬──┬──┘
                           │  │  │
                           │  │  └──────── lifecycle ─────────┐
                           │  │                               │
                           ▼  ▼                               ▼
                        Core Agent                   Relay / Feed / Press
                           │                               │
                           └──────────────┐                │
                                          ▼                ▼
                                     Applications / Services

                         ┌────────────────────────┐
                         │       Yasin-AI         │
                         │ Independent AI Platform│
                         ├──────────┬─────────────┤
                         │Knowledge │ Memory      │
                         │API/Run.  │ Extensions  │
                         └──────────┴─────────────┘
```

## 22. Rules for a New AI Agent

Before changing any Yasin repository, an AI agent must:

1. identify which project owns the requested behavior;
2. inspect that project's public contracts and tests;
3. classify the relationship as runtime, SDK/API, operational, or conceptual;
4. avoid introducing a cross-project dependency without an explicit contract;
5. preserve the distinction between local application state and ecosystem memory;
6. use Hub for ecosystem operational coordination rather than importing Hub internals;
7. use YasinCLI as the unified user-facing surface rather than duplicating project internals;
8. preserve provider abstractions in Relay/Feed/Press;
9. treat Yasin-AI as an independent platform unless a documented integration contract says otherwise;
10. update YASIN-DOCS and an ADR when a cross-project architectural boundary changes.

## 23. Open Architectural Decisions

1. Should Yasin-AI integrate with Yasin-Core through a formal SDK contract?
2. Should YasinCLI gain first-class adapters for AI, Feed, and Press?
3. Should YasinFeed become a reusable content foundation for YasinPress?
4. Should AI providers be centralized behind a provider gateway?
5. Should the ecosystem introduce a global event bus?
6. Should shared ecosystem memory be introduced separately from application-local state?
7. What exact API/protocol should exist between YasinCLI and YasinHub?
8. Which project should be authoritative for ecosystem registry metadata?

These are **open decisions**, not current dependencies.

## 24. Documentation Governance

This file is the canonical architecture baseline. Project-specific documents may provide deeper detail but must not contradict it without an ADR or explicit architecture update.

Recommended hierarchy:

```text
YASIN-DOCS
├── Canonical Ecosystem Architecture
├── Dependency Matrix
├── Project Architecture
│   ├── Core
│   ├── Agent
│   ├── AI
│   ├── Hub
│   ├── CLI
│   ├── Relay
│   ├── Feed
│   └── Press
├── ADRs
├── API Contracts
├── Operational Runbooks
└── Release / Compatibility Matrix
```

## 25. Status

**Canonical Architecture v1 is established as the current documentation baseline.**

The baseline is deliberately conservative: confirmed dependencies are recorded as dependencies, uncertain relationships are marked unresolved, and future architecture is represented as proposals/open questions rather than facts.
