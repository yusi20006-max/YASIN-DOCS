# Yasin Ecosystem — Canonical Architecture v1

> Canonical architecture baseline for the Yasin ecosystem. This document gives engineers and AI coding agents the system-level model for project roles, ownership, boundaries, dependencies, operational control, and integration rules.

- Status: Canonical Draft v1.1
- Date: 2026-08-14
- Evidence policy: confirmed source-level relationships are distinguished from intended architecture, proposed integrations, and unresolved decisions.

## 1. Executive Summary

Yasin is a multi-project ecosystem, not a monolithic application. The architecture separates five major concerns:

1. **Core runtime** — Yasin-Core provides generic runtime and SDK foundations.
2. **Agent execution** — Yasin-Agent provides agent/workflow execution on top of Core.
3. **AI platform** — Yasin-AI is the **canonical AI platform for the ecosystem**. It owns shared AI capabilities such as model/provider routing, inference-facing services, knowledge, embeddings, RAG primitives, durable AI memory, AI extensions, AI observability, and AI-facing APIs/contracts.
4. **Control/operations** — YasinHub provides ecosystem lifecycle control, status, health, and operational integration.
5. **Unified user interface** — YasinCLI provides the user-facing command surface and ecosystem orchestration.

Content applications form another family:

- YasinRelay — Telegram/content relay and publishing pipeline.
- YasinFeed — general content aggregation/processing/publishing platform.
- YasinPress — specialized Persian-news publishing automation.

### Architectural intent for AI

Yasin-AI is independent in **runtime ownership** but central in **AI capability ownership**. Applications and agent systems must not recreate ecosystem-wide AI infrastructure independently when the capability belongs in Yasin-AI. They should consume Yasin-AI through explicit, versioned public contracts rather than importing private implementation modules.

This is a target architectural direction being formalized now. Existing local provider abstractions in Relay/Feed/Press remain valid until their migration contracts are explicitly introduced.

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
        │        │          │
        │        │     ┌────┼────┐
        │        │     ▼    ▼    ▼
        │        │   Relay Feed Press
        │        │     │    │    │
        └────────┼─────┴────┴────┘
                 │
                 ▼
        AI capability contracts
                 │
                 ▼
        ┌─────────────────────┐
        │      Yasin-AI       │
        │ Canonical AI Plane  │
        ├─────────────────────┤
        │ Model/Provider      │
        │ Inference Services  │
        │ Knowledge / RAG     │
        │ Embeddings          │
        │ Durable AI Memory   │
        │ AI Extensions       │
        │ AI Observability    │
        │ AI API / SDK        │
        └─────────────────────┘
```

Yasin-AI is not required to import YasinHub in order to execute. YasinHub controls and observes it through public operational boundaries.

## 3. Project Responsibility Matrix

| Project | Primary responsibility | Operationally controlled by | AI relationship |
|---|---|---|---|
| `Yasin-Core` | Generic runtime + SDK foundation | Hub / CLI | May consume AI contracts; must not own ecosystem-wide AI infrastructure |
| `Yasin-Agent` | Agent/workflow execution | Hub / CLI | Consumes Yasin-AI capabilities through public contracts where AI is required |
| `Yasin-AI` | Canonical ecosystem AI platform | Hub / CLI | Owns shared AI capabilities |
| `YasinHub` | Control + observability + lifecycle | Operator / CLI | Controls/observes AI through public operational contracts |
| `YasinCLI` | Unified UX + ecosystem orchestration | Operator | Provides user-facing access to AI through adapters, not duplicated internals |
| `YasinRelay` | Content ingestion/transformation/publishing | Hub / CLI | Uses AI capability contract; local provider abstraction is transitional |
| `YasinFeed` | General content aggregation/processing/publishing | Hub / CLI | Uses AI capability contract; provider adapters are transitional |
| `YasinPress` | Specialized Persian news automation | Hub / CLI | Uses AI capability contract; local provider integration is transitional |

## 4. Dependency and Integration Model

The ecosystem distinguishes **runtime dependency**, **control relationship**, and **capability consumption**.

```text
Runtime dependency:
Agent ─────→ Core

Control relationship:
CLI ─────→ Hub ─────→ project runtimes

AI capability consumption:
Core / Agent / Relay / Feed / Press / future services
                  │
                  ▼
        versioned AI contract
                  │
                  ▼
              Yasin-AI
```

Consuming Yasin-AI does not imply importing its private Python modules. The intended boundary is a public API/SDK/protocol/provider contract.

## 5. Confirmed vs Target Relationships

The following distinction is mandatory:

- **Confirmed** — backed by repository/source evidence today.
- **Target** — intentional ecosystem architecture that implementation must converge toward.
- **Proposed** — candidate design not yet selected.
- **Unresolved** — requires a decision or contract before implementation.

### Confirmed today

```text
Yasin-Agent ───────────────→ Yasin-Core
YasinHub ──────────────────→ Yasin-Core SDK
YasinHub ──────────────────→ Yasin-Agent SDK
```

### Target architecture

```text
Yasin-AI = canonical ecosystem AI capability platform

Yasin-Agent ──AI contract──→ Yasin-AI
YasinRelay ───AI contract──→ Yasin-AI
YasinFeed ────AI contract──→ Yasin-AI
YasinPress ───AI contract──→ Yasin-AI
YasinCLI ─────AI adapter────→ Yasin-AI
YasinHub ─────control/report→ Yasin-AI
```

These target edges must be implemented only through explicit public contracts and compatibility rules.

## 6. Yasin-Core

### Mission

Provide reusable runtime and SDK foundations for the ecosystem.

### Boundary

Core is a foundation layer. Higher-level AI platform concerns belong in Yasin-AI rather than being duplicated inside Core.

```text
Core → runtime / SDK foundations
Core ✕ Hub internals
Core ✕ application business logic
Core ✕ duplicate ecosystem-wide AI provider infrastructure
```

Core may expose generic execution/tool/provider contracts that allow integration with Yasin-AI, but Core does not become the owner of Yasin-AI functionality.

## 7. Yasin-Agent

### Mission

Provide agent and workflow execution capabilities.

### Core relationship

The audit confirms Agent → Core. Agent is therefore a runtime/application layer built on the generic Core foundation.

### AI relationship

Agent owns planning/execution semantics, not the ecosystem AI platform. When it needs model inference, knowledge, memory, embeddings, or other shared AI capabilities, the target architecture is to consume Yasin-AI through a public contract.

```text
Yasin-Agent
   ├── execution/workflows
   └── AI capability contract
                 ↓
             Yasin-AI
```

## 8. Yasin-AI — Canonical AI Platform

### Mission

Yasin-AI is the central AI capability platform of the Yasin ecosystem. Its purpose is to prevent every project from independently implementing model routing, provider management, inference services, knowledge/RAG, embeddings, durable AI memory, AI extensions, evaluation/observability, and related AI infrastructure.

### Ownership

Yasin-AI owns:

- model/provider abstraction and routing;
- inference-facing AI services;
- prompts and AI execution policies where platform-owned;
- embeddings and semantic retrieval primitives;
- knowledge/RAG capabilities;
- durable AI memory;
- AI extension/plugin contracts;
- AI-specific observability and diagnostics;
- AI service/API/SDK contracts;
- provider fallback, health, and reliability policies where centralized by the platform.

### Non-ownership

Yasin-AI does **not** own:

- application business logic;
- news aggregation rules;
- Telegram/Eitaa publishing workflows;
- ecosystem lifecycle orchestration;
- the generic runtime foundation;
- agent workflow semantics.

### Independence rule

Yasin-AI is independently runnable and must not require Hub, CLI, Feed, Press, Relay, or Agent internals to execute its core AI capabilities.

At the same time, it is the **canonical provider of shared AI capabilities** for those projects through public contracts.

### Persistence

SQLite may remain the default local persistence mechanism for Yasin-AI memory and semantic indexes. This platform-owned durable state is distinct from application-local state in Feed, Press, Relay, and other applications.

### Plugin security

Current plugin execution is trusted/in-process. Remote untrusted execution is not established as supported. Sandboxing and stronger authorization remain separate security evolution work.

## 9. YasinHub

### Mission

YasinHub is the ecosystem control and observability plane.

### Responsibilities

- status aggregation;
- process and health detection;
- lifecycle commands;
- Core SDK integration;
- Agent SDK integration;
- application operational controls;
- AI platform operational controls/registration;
- ecosystem registry;
- dashboard/doctor-style operator visibility.

### Boundary

Hub controls projects but does not own their internal business logic or AI implementation.

```text
Hub
 ↓ public SDK/API/process contract
Project runtime
```

Yasin-AI should expose an operational contract that lets Hub inspect health/capabilities/version and perform supported lifecycle operations without importing Yasin-AI internals.

## 10. YasinCLI

### Mission

Provide a unified user-facing command surface across the ecosystem.

### Architectural role

YasinCLI is not a second implementation of each project's internals. It uses adapters and orchestration and delegates project-specific behavior to the appropriate boundary.

For AI operations, the intended path is:

```text
User
 ↓
YasinCLI
 ↓
AI adapter / Hub public API
 ↓
Yasin-AI
```

The CLI must not duplicate provider routing, memory, RAG, or model-management logic.

## 11. YasinRelay

### Mission

Content ingestion, transformation, and publication pipeline.

### AI boundary

Relay currently owns an `AIProcessor` abstraction. This remains a valid application boundary during migration. The target architecture is for the abstraction to delegate to Yasin-AI through a versioned AI capability contract when the contract is implemented.

Relay must retain ownership of content pipeline semantics; Yasin-AI must not absorb Relay business logic.

## 12. YasinFeed

### Mission

General-purpose content aggregation, processing, storage, rewriting, and publishing.

### AI boundary

Feed owns its application pipeline. AI rewriting, translation, classification, summarization, and related intelligence should converge on Yasin-AI capability contracts rather than proliferating independent provider implementations.

Feed remains independently runnable.

## 13. YasinPress

### Mission

Specialized Persian-news publishing automation.

### AI boundary

Press owns news-specific policy and publishing logic. AI tasks such as rewriting, classification assistance, summarization, prioritization assistance, or model/provider routing should converge on Yasin-AI through explicit contracts.

Existing optional/local AI integrations remain valid until migration work is completed.

## 14. Storage Architecture

There is intentionally no confirmed shared application database.

```text
Yasin-AI    → durable platform AI memory / semantic indexes
YasinRelay  → pipeline-state SQLite
YasinFeed   → application storage
YasinPress  → application-state SQLite
```

Yasin-AI memory must not silently become a shared application database. If ecosystem-wide memory is introduced, it requires an explicit contract and ADR.

## 15. AI Provider Architecture

The target architecture centralizes ecosystem-wide AI capability ownership in Yasin-AI:

```text
                    Yasin-AI
                       │
              AI Provider Gateway
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Cloud APIs    Local Models   Other Providers
          │            │            │
          └────────────┼────────────┘
                       ▼
             Common AI capability API
                       ▲
          ┌────────────┼────────────┐
          │            │            │
       Agent        Feed/Press    Relay
```

Provider implementations may remain local during migration, but new ecosystem-wide provider logic should not be duplicated in application repositories when it belongs in Yasin-AI.

## 16. Event Architecture

Current confirmed scopes remain:

```text
Relay internal events → local pipeline scope
Hub status contract   → ecosystem operational scope
Project SDK/API       → explicit control scope
```

There is no confirmed global event bus. Yasin-AI may expose AI lifecycle/usage events through its own contract, but a global ecosystem bus requires schema/versioning, delivery semantics, retries, idempotency, security, ownership, and an ADR.

## 17. Security Boundaries

Security responsibilities remain local to each boundary:

- Core: runtime security contracts;
- Agent: execution/tool security;
- AI: provider credentials, plugin trust, AI API/service security, memory access;
- Hub: operator/control authorization;
- CLI: local credential/config handling;
- Feed/Press/Relay: provider credentials and publishing permissions.

Centralizing AI capabilities in Yasin-AI does not mean centralizing every project's authorization model.

## 18. Lifecycle Model

```text
YasinCLI
   ↓
YasinHub
   ↓
start / stop / restart / health / doctor
   ↓
Yasin-AI and project-specific runtimes
```

The project owns execution semantics; Hub owns ecosystem-level operational coordination.

## 19. Dependency Direction Rules

### Allowed

```text
Application → public AI capability contract → Yasin-AI
Agent → Core
Agent → public AI capability contract → Yasin-AI
Hub → public project/AI SDK or API
CLI → adapters / public APIs
```

### Discouraged / prohibited without explicit contract

```text
Core → Hub
Core → application internals
Agent → Hub internals
Project → Hub internal modules
Project → Yasin-AI private modules
Shared database → implicit cross-project coupling
```

### AI rule

If a capability is ecosystem-wide AI infrastructure, implement it in Yasin-AI first and expose it through a public contract. Do not create parallel provider routers, shared AI memory systems, or duplicate AI platform infrastructure inside Feed/Press/Relay/Agent unless there is an explicit documented exception.

## 20. Canonical Terms

| Term | Meaning |
|---|---|
| Runtime Plane | Execution logic of an individual project |
| Control Plane | Ecosystem lifecycle and operational coordination |
| Observability Plane | Status, health, metrics, and diagnostics |
| AI Plane | Shared AI capabilities owned by Yasin-AI |
| Platform | Reusable capability boundary such as Core or AI |
| Application | Product-specific pipeline such as Feed, Press, or Relay |
| Adapter | Integration boundary around another service/provider |
| Operational State | Local state required to run a project |
| Ecosystem Memory | Shared durable memory only if explicitly introduced |
| AI Capability Contract | Versioned public interface through which projects consume Yasin-AI |

## 21. Current-to-Target Graph

```text
                              OPERATOR
                                 │
                                 ▼
                           YasinCLI
                                 │
                                 ▼
                           YasinHub
                     Control / Status / Lifecycle
                       ┌─────────┼─────────┐
                       ▼         ▼         ▼
                     Core      Agent   Applications
                       │         │      ┌──┼──┐
                       │         │      ▼  ▼  ▼
                       │         │    Relay Feed Press
                       │         │      │    │    │
                       └─────────┼──────┴────┴────┘
                                 │
                         AI Capability Contract
                                 │
                                 ▼
                           Yasin-AI
                    Canonical AI Platform
                ┌────────┼──────────┬────────┐
                ▼        ▼          ▼        ▼
             Models   Knowledge   Memory  AI API/SDK
                │        │          │        │
                └────────┴──────────┴────────┘
                         AI Providers
```

## 22. Rules for a New AI Agent

Before changing any Yasin repository, an AI agent must:

1. identify which project owns the requested behavior;
2. inspect that project's public contracts and tests;
3. read this canonical architecture and the dependency matrix;
4. classify the relationship as runtime, SDK/API, operational, or AI capability consumption;
5. avoid introducing a cross-project dependency without an explicit contract;
6. preserve the distinction between local application state and Yasin-AI platform memory;
7. use Hub for ecosystem operational coordination rather than importing Hub internals;
8. use YasinCLI as the unified user-facing surface rather than duplicating project internals;
9. treat Yasin-AI as the canonical owner of ecosystem-wide AI infrastructure;
10. consume Yasin-AI through public/versioned contracts, never private modules;
11. preserve provider abstractions in Relay/Feed/Press while migrating them toward the canonical AI contract;
12. update YASIN-DOCS and an ADR when a cross-project architectural boundary changes.

## 23. Open Architectural Decisions

1. What is the first versioned AI Capability Contract (API/SDK/protocol) exposed by Yasin-AI?
2. Should Yasin-AI consume selected generic primitives from Yasin-Core, or remain implementation-independent?
3. How should Yasin-Agent integrate with Yasin-AI while keeping execution semantics in Agent?
4. Should YasinCLI gain a first-class Yasin-AI adapter?
5. What exact operational API should YasinHub use for Yasin-AI?
6. Which AI capabilities are mandatory for all applications versus optional?
7. How should existing Relay/Feed/Press local providers migrate to Yasin-AI?
8. Should Yasin-AI memory remain AI-platform memory or evolve into an explicitly shared ecosystem memory service?
9. Should the ecosystem introduce a global event bus?
10. What compatibility/version policy governs AI capability contracts?

These are implementation/design decisions remaining after the strategic decision that **Yasin-AI is the canonical ecosystem AI platform**.

## 24. Documentation Governance

This file is the canonical system-level architecture. Project-specific documents may provide deeper detail but must not contradict it without an ADR or explicit architecture update.

When the AI platform boundary changes, update:

1. this canonical architecture;
2. the dependency matrix;
3. the Yasin-AI project architecture;
4. the relevant API/compatibility contract;
5. an ADR recording the decision and migration impact.

## 25. Status

**Canonical Architecture v1.1 establishes Yasin-AI as the canonical AI capability platform for the Yasin ecosystem.**

The architecture intentionally separates:

- Core runtime ownership;
- Agent execution ownership;
- AI capability ownership;
- ecosystem control/observability;
- application business logic.

Implementation must converge toward this model through explicit public contracts rather than hidden cross-project coupling.
