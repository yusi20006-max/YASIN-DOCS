# Yasin Ecosystem — Cross-Project Dependency Matrix v1

- Date: 2026-08-10
- Status: Working architecture baseline
- Evidence: source-verified where marked CONFIRMED; unresolved edges are intentionally not inferred.

## Scope

This matrix consolidates the completed audits for Yasin-Core, Yasin-Agent, Yasin-AI, YasinHub, YasinCLI, YasinRelay, YasinFeed, and YasinPress.

YasinFeed and YasinPress are explicitly documented as **independent application runtimes**. Neither is a runtime dependency of the other.

## Role Matrix

| Project | Primary Role | Plane | Runtime Owner? | Standalone? |
|---|---|---|---:|---:|
| Yasin-Core | Generic ecosystem runtime + SDK | Runtime/Foundation | Yes | Yes |
| Yasin-Agent | Agent definitions + workflow execution | Agent/Application | Yes, at workflow level | Yes, with Core |
| Yasin-AI | AI runtime, knowledge, memory, API, extensions | AI Platform | Yes | Yes |
| YasinHub | Ecosystem control + observability | Control Plane | Orchestrates; does not own project runtimes | Yes |
| YasinCLI | Unified user interface + lifecycle orchestration | User/Orchestration Plane | No | Yes |
| YasinRelay | Content ingestion → AI processing → publishing | Application/Data Pipeline | Yes | Yes |
| YasinFeed | General content aggregation/processing/publishing | Application/Data Pipeline | Yes | Yes |
| YasinPress | Specialized Persian-news publishing | Application/Data Pipeline | Yes | Yes |

## Dependency Legend

- **DIRECT**: source-level import/package/SDK dependency.
- **CONTROL**: orchestration through a public integration boundary.
- **REPORT**: status/observability relationship.
- **CONTRACT**: shared protocol/interface without runtime ownership.
- **UNVERIFIED**: no evidence; do not infer a dependency.
- **NONE REQUIRED**: the project is intentionally independent of that target at runtime.

## Matrix

| From ↓ / To → | Core | Agent | AI | Hub | CLI | Relay | Feed | Press |
|---|---|---|---|---|---|---|---|---|
| Core | — | DIRECT | UNVERIFIED | None required | Consumed | NONE REQUIRED | NONE REQUIRED | NONE REQUIRED |
| Agent | DIRECT | — | UNVERIFIED | None required | Consumed | NONE REQUIRED | NONE REQUIRED | NONE REQUIRED |
| AI | UNVERIFIED | UNVERIFIED | — | REPORT/registry | Adapter gap | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| Hub | DIRECT SDK | DIRECT SDK | REPORT/registry | — | CONTROL surface | CONTROL/registry | CONTROL/registry | CONTROL/registry |
| CLI | Adapter/CONTROL | Adapter/CONTROL | Adapter gap | CONTROL | — | Adapter/CONTROL | Adapter/CONTROL | Adapter/CONTROL |
| Relay | UNVERIFIED | UNVERIFIED | Local AI boundary | REPORT/registry | Adapter/CONTROL | — | NONE REQUIRED | NONE REQUIRED |
| Feed | UNVERIFIED | UNVERIFIED | Local AI boundary | REPORT/registry | Adapter/CONTROL | NONE REQUIRED | — | NONE REQUIRED |
| Press | UNVERIFIED | UNVERIFIED | Local AI boundary | REPORT/registry | Adapter/CONTROL | NONE REQUIRED | NONE REQUIRED | — |

## Core ↔ Agent

```text
Yasin-Core
  ├── BaseAgent
  ├── Context
  ├── Client / SDK
  ├── Memory API
  └── Tool contracts
          ↓
Yasin-Agent Adapter
  ├── AgentDefinition
  ├── Planner
  ├── Executor
  └── ToolRunner
```

Core provides runtime-facing contracts and infrastructure; Agent provides application-level planning and execution.

## Hub Control Plane

```text
                    YasinHub
                  /    |     \
                 /     |      \
             Core     Agent   Applications
                              ├─ Relay
                              ├─ Feed
                              └─ Press
```

Hub controls and observes through public boundaries; project runtimes should not require Hub in order to execute.

## CLI Position

```text
Operator
   ↓
YasinCLI
   ↓
Adapters / public APIs
   ↓
YasinHub / Core / Agent / Relay / Feed / Press / ...
```

YasinCLI is the top-level user-facing command surface. Hub remains the operational control plane. CLI must not duplicate Hub's internal process-management implementation.

## Independent Application Boundary

YasinFeed and YasinPress have intentionally separate runtime boundaries:

```text
                    ┌─────────────────┐
                    │   YasinFeed     │
                    │ standalone app  │
                    └─────────────────┘

                    ┌─────────────────┐
                    │   YasinPress    │
                    │ standalone app  │
                    └─────────────────┘
```

There is no Feed → Press or Press → Feed runtime dependency. They may eventually share a library, protocol, or provider gateway, but such reuse must be explicit and must not make either application require the other to run.

## Yasin-AI Boundary

Repository-wide source inspection found no direct `yasin_core` dependency in Yasin-AI. Therefore no direct AI → Core edge is documented.

Yasin-AI owns its own platform layers:

```text
Runtime
Knowledge
Memory
Developer Platform
API Service
Observability
Deployment
```

Its durable memory/persistence responsibility remains distinct from application-local state in Core, Relay, Feed, and Press until an explicit bridge is designed.

## YasinRelay Boundary

```text
Telegram
   ↓
Collector
   ↓
Normalizer
   ↓
Validator
   ↓
Deduplication / SQLite
   ↓
AI Processor
   ↓
Media Preparation
   ↓
Eitaa Publisher
```

Relay's AI provider configuration is currently an application-local boundary. No direct Yasin-AI dependency is claimed without source evidence.

## YasinFeed Boundary

```text
Sources
   ↓
Fetch / Normalize
   ↓
Process / Rewrite / Translate
   ↓
Storage
   ↓
Publisher
   ├─ RSS
   ├─ PWA/API
   └─ Eitaa
```

Feed owns its pipeline and application state. It can execute without Press.

## YasinPress Boundary

```text
RSS
 ↓
Collection
 ↓
Duplicate / Age / Category / Priority / Breaking
 ↓
Optional AI
 ↓
Formatter / Tags / Digest
 ↓
Durable Queue
 ↓
Rate Limiter
 ↓
Eitaa Publisher
```

Press owns its pipeline and application state. It can execute without Feed.

## Dependency Direction Rules

1. Core remains below Agent and other runtime consumers.
2. Agent may consume Core SDK contracts; Core must not depend on Agent.
3. Hub may control/observe runtimes through public APIs/SDKs; runtimes should not require Hub to execute.
4. CLI is the user-facing aggregation layer and delegates rather than duplicates project internals.
5. AI is not attached to Core merely because both provide AI/runtime functionality.
6. Relay, Feed, and Press may use AI providers without implying ownership by Yasin-AI.
7. Feed and Press must remain independently runnable; neither may become a hidden runtime dependency of the other.
8. Shared status contracts are not the same as Python/runtime dependencies.
9. Every cross-project dependency in the final architecture must be backed by an explicit import, package dependency, protocol, API, or documented operational contract.

## Cycles to Prevent

```text
Core → Hub → Core
Agent → Hub → Agent
CLI → Hub → CLI
Core → Agent → Core
Feed → Press → Feed
Feed → Hub internals → Feed
Press → Hub internals → Press
```

## Current High-Level Graph

```text
                             OPERATOR
                                │
                                ▼
                           YasinCLI
                     Unified UX / Commands
                                │
                                ▼
                           YasinHub
                         Control / Status
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
                  Core        Agent    Applications
                                         │
                              ┌──────────┼──────────┐
                              ▼          ▼          ▼
                           Relay      Feed       Press
                              │          │          │
                         local AI   local AI    local AI

                         Yasin-AI
                   independent AI platform
                   Knowledge / Memory / API
```

## Unresolved Questions

1. Should Yasin-AI eventually consume Core SDK or remain independent?
2. Should Yasin-AI memory integrate with Core memory, or remain a separate platform service?
3. Should YasinCLI gain first-class AI/Feed/Press adapters?
4. Should Hub expose a stable machine-readable control API for CLI?
5. Which project is the canonical owner of model/provider routing?
6. What is the canonical versioned status protocol?
7. Should Relay eventually delegate AI processing to Yasin-AI?
8. Should Feed and Press eventually share a reusable content library without creating a runtime dependency?
9. Which repositories constitute official Yasin ecosystem membership?

## Next Audit Order

1. Complete/verify dedicated YasinFeed audit.
2. Complete/verify dedicated YasinPress audit.
3. Cross-project verification against package/import/test evidence.
4. Canonical ecosystem graph v2.
5. Target architecture and migration boundaries.
6. Final ADR index and ecosystem architecture document.
