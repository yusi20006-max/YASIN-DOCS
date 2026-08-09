# Yasin Ecosystem — Cross-Project Dependency Matrix v1

- Date: 2026-08-10
- Status: Working architecture baseline
- Evidence: source-verified where marked CONFIRMED; unresolved edges are intentionally not inferred.

## Scope

This matrix consolidates the completed audits for Yasin-Core, Yasin-Agent, Yasin-AI, YasinHub, YasinCLI, and YasinRelay. YasinFeed and YasinPress remain outside the source-verified dependency matrix until their dedicated audits are completed.

## Role Matrix

| Project | Primary Role | Plane | Runtime Owner? |
|---|---|---|---:|
| Yasin-Core | Generic ecosystem runtime + SDK | Runtime/Foundation | Yes |
| Yasin-Agent | Agent definitions + workflow execution | Agent/Application | Yes, at workflow level |
| Yasin-AI | AI runtime, knowledge, memory, API, extensions | AI Platform | Yes |
| YasinHub | Ecosystem control + observability | Control Plane | Orchestrates; does not own project runtimes |
| YasinCLI | Unified user interface + lifecycle orchestration | User/Orchestration Plane | No |
| YasinRelay | Content ingestion → AI processing → publishing | Application/Data Pipeline | Yes |

## Dependency Legend

- **DIRECT**: source-level import/package/SDK dependency.
- **CONTROL**: orchestration through a public integration boundary.
- **REPORT**: status/observability relationship.
- **CONTRACT**: shared protocol/interface without runtime ownership.
- **UNVERIFIED**: no evidence; do not infer a dependency.

## Matrix

| From ↓ / To → | Core | Agent | AI | Hub | CLI | Relay |
|---|---|---|---|---|---|---|
| Core | — | DIRECT | UNVERIFIED | None required | Consumed | UNVERIFIED |
| Agent | DIRECT | — | UNVERIFIED | None required | Consumed | UNVERIFIED |
| AI | UNVERIFIED | UNVERIFIED | — | REPORT/registry | Adapter gap | Local capability |
| Hub | DIRECT SDK | DIRECT SDK | REPORT/registry | — | CONTROL surface | CONTROL/registry |
| CLI | Adapter/CONTROL | Adapter/CONTROL | Adapter gap | CONTROL | — | Adapter/CONTROL |
| Relay | UNVERIFIED | UNVERIFIED | Local AI boundary | REPORT/registry | Adapter/CONTROL | — |

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
                  /          \
             Core SDK       Agent SDK
                ↓              ↓
           Core Runtime    Agent Runtime
```

Hub controls and observes through public boundaries; Core and Agent should not require Hub in order to execute.

Hub also monitors process state and shared status records for projects such as Relay, Feed, AI, and Press.

## CLI Position

```text
Operator
   ↓
YasinCLI
   ↓
Adapters / public APIs
   ↓
YasinHub / Core / Agent / Relay / ...
```

YasinCLI is the top-level user-facing command surface. Hub remains the operational control plane. CLI must not duplicate Hub's internal process-management implementation.

The audited CLI currently has first-class adapters for Core, Agent, Hub, and Relay. AI, Feed, and Press are current adapter coverage gaps; this does not prove they cannot be controlled.

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

Its durable memory/persistence responsibility remains distinct from Core runtime memory until an explicit bridge is designed.

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

## Dependency Direction Rules

1. Core remains below Agent and other runtime consumers.
2. Agent may consume Core SDK contracts; Core must not depend on Agent.
3. Hub may control/observe runtimes through public APIs/SDKs; runtimes should not require Hub to execute.
4. CLI is the user-facing aggregation layer and delegates rather than duplicates project internals.
5. AI is not attached to Core merely because both provide AI/runtime functionality.
6. Relay may use AI providers without implying ownership by Yasin-AI.
7. Shared status contracts are not the same as Python/runtime dependencies.
8. Every cross-project dependency in the final architecture must be backed by an explicit import, package dependency, protocol, API, or documented operational contract.

## Cycles to Prevent

```text
Core → Hub → Core
Agent → Hub → Agent
CLI → Hub → CLI
Core → Agent → Core
```

## Current High-Level Graph

```text
                             OPERATOR
                                │
                                ▼
                           YasinCLI
                     Unified UX / Commands
                       │       │       │
                       │       │       └──────────────┐
                       │       │                      │
                       ▼       ▼                      ▼
                    YasinHub  Core/SDK            Relay Adapter
                       │
             ┌─────────┼─────────┐
             ▼         ▼         ▼
           Core      Agent      Relay
             │         │         │
             │         │         └── local AI provider
             │         │
             └─────────┘

             Yasin-AI
       independent AI platform
       Knowledge / Memory / API

   Shared status/operations plane:
       Core / Agent / AI / Relay / Feed / Press ...
                         ↓
                      YasinHub
```

## Unresolved Questions

1. Should Yasin-AI eventually consume Core SDK or remain independent?
2. Should Yasin-AI memory integrate with Core memory, or remain a separate platform service?
3. Should YasinCLI gain first-class AI/Feed/Press adapters?
4. Should Hub expose a stable machine-readable control API for CLI?
5. Which project is the canonical owner of model/provider routing?
6. What is the canonical versioned status protocol?
7. Should Relay eventually delegate AI processing to Yasin-AI?
8. Which repositories constitute official Yasin ecosystem membership?

## Next Audit Order

1. YasinRelay deep audit.
2. YasinFeed audit.
3. YasinPress audit.
4. Cross-project verification against package/import/test evidence.
5. Canonical ecosystem graph v2.
6. Target architecture and migration boundaries.
7. Final ADR index and ecosystem architecture document.
