# Yasin Ecosystem — Cross-Project Dependency Matrix v1

- Date: 2026-08-14
- Status: Working architecture baseline v1.1
- Strategic AI decision: **Yasin-AI is the canonical AI capability platform for the ecosystem.**

## Scope

This matrix covers Yasin-Core, Yasin-Agent, Yasin-AI, YasinHub, YasinCLI, YasinRelay, YasinFeed, and YasinPress.

Yasin-AI is independently runnable, but it is the canonical owner of shared ecosystem-wide AI capabilities. Projects consume those capabilities through versioned public contracts; this does not imply imports of private Yasin-AI modules.

## Legend

- **DIRECT**: source-level import/package/SDK dependency.
- **CONTROL**: orchestration through a public boundary.
- **REPORT**: status/observability relationship.
- **AI-CONTRACT**: target consumption of Yasin-AI through a public/versioned AI interface.
- **ADAPTER**: integration/user-facing adapter.
- **UNVERIFIED**: no current implementation evidence.
- **NONE REQUIRED**: intentionally independent runtime.

## Role Matrix

| Project | Primary Role | Plane | AI Role |
|---|---|---|---|
| Yasin-Core | Generic runtime + SDK | Runtime/Foundation | Generic runtime contracts; not AI platform owner |
| Yasin-Agent | Agent/workflow execution | Agent/Application | Target AI consumer |
| Yasin-AI | AI runtime, knowledge, memory, API, extensions | AI Platform | **Canonical AI capability owner** |
| YasinHub | Ecosystem control + observability | Control Plane | Controls/observes AI platform |
| YasinCLI | Unified UX + lifecycle orchestration | User/Orchestration | Target first-class AI adapter |
| YasinRelay | Content ingestion → processing → publishing | Application | Target AI consumer; local AI boundary transitional |
| YasinFeed | Content aggregation/processing/publishing | Application | Target AI consumer; local providers transitional |
| YasinPress | Persian-news publishing | Application | Target AI consumer; local AI integration transitional |

## Matrix

| From ↓ / To → | Core | Agent | AI | Hub | CLI | Relay | Feed | Press |
|---|---|---|---|---|---|---|---|---|
| Core | — | DIRECT | UNVERIFIED | None required | Consumed | NONE REQUIRED | NONE REQUIRED | NONE REQUIRED |
| Agent | DIRECT | — | **AI-CONTRACT (TARGET)** | None required | Consumed | NONE REQUIRED | NONE REQUIRED | NONE REQUIRED |
| AI | UNVERIFIED | UNVERIFIED | — | **REPORT/CONTROL (TARGET)** | **ADAPTER (TARGET)** | AI provider | AI provider | AI provider |
| Hub | DIRECT SDK | DIRECT SDK | **REPORT/CONTROL (TARGET)** | — | CONTROL | CONTROL/registry | CONTROL/registry | CONTROL/registry |
| CLI | Adapter/CONTROL | Adapter/CONTROL | **ADAPTER (TARGET)** | CONTROL | — | Adapter/CONTROL | Adapter/CONTROL | Adapter/CONTROL |
| Relay | UNVERIFIED | UNVERIFIED | **AI-CONTRACT (TARGET)** | REPORT/registry | Adapter/CONTROL | — | NONE REQUIRED | NONE REQUIRED |
| Feed | UNVERIFIED | UNVERIFIED | **AI-CONTRACT (TARGET)** | REPORT/registry | Adapter/CONTROL | NONE REQUIRED | — | NONE REQUIRED |
| Press | UNVERIFIED | UNVERIFIED | **AI-CONTRACT (TARGET)** | REPORT/registry | Adapter/CONTROL | NONE REQUIRED | NONE REQUIRED | — |

## Canonical AI Boundary

```text
                    Yasin-AI
               Canonical AI Platform
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
   Provider Routing  Knowledge/RAG    Memory
        │               │                │
        └───────────────┼────────────────┘
                        ▼
                AI Capability API
                        ▲
        ┌───────────────┼───────────────┐
        │               │               │
      Agent        Feed/Press         Relay
```

## Application AI Boundary

Current local AI/provider implementations remain valid as transitional boundaries:

```text
Relay  → local AIProcessor → target Yasin-AI contract
Feed   → local provider adapters → target Yasin-AI contract
Press  → local/Cloudflare AI → target Yasin-AI contract
Agent  → execution logic → target Yasin-AI contract
```

Applications retain their own business logic and pipelines.

## Control and CLI

```text
Operator → YasinCLI → adapters/public APIs → YasinHub / Yasin-AI / projects
```

Hub remains the ecosystem control plane. CLI must not duplicate AI provider, memory, RAG, or model-management internals.

## Storage Boundary

```text
Yasin-AI    → AI platform memory / semantic indexes
YasinRelay  → pipeline state
YasinFeed   → application storage
YasinPress  → application state
```

No shared application database is implied.

## Dependency Direction Rules

1. Core remains below Agent and runtime consumers.
2. Agent may consume Core; Core must not depend on Agent.
3. Hub controls/observes through public APIs/SDKs; runtimes should not require Hub.
4. CLI delegates rather than duplicating project internals.
5. Yasin-AI owns ecosystem-wide AI platform capabilities.
6. Projects consume Yasin-AI through public/versioned AI contracts, not private modules.
7. Relay/Feed/Press may retain local AI adapters during migration; new shared AI infrastructure belongs in Yasin-AI.
8. Feed and Press remain independently runnable.
9. Status contracts are not automatically runtime dependencies.
10. Every implemented cross-project dependency must have explicit source or contract evidence.

## Cycles to Prevent

```text
Core → Hub → Core
Agent → Hub → Agent
CLI → Hub → CLI
Core → Agent → Core
Feed → Press → Feed
Application → Yasin-AI private modules → Application
```

## Unresolved Contract Work

1. First version of the Yasin-AI Capability API/SDK/protocol.
2. Yasin-AI ↔ Yasin-Core boundary.
3. Yasin-Agent ↔ Yasin-AI contract.
4. YasinHub ↔ Yasin-AI operational API.
5. YasinCLI first-class AI adapter.
6. Relay/Feed/Press migration strategy.
7. AI capability catalog and compatibility/version policy.
8. Future scope of Yasin-AI memory.
9. Possible global event bus.

## Status

This matrix now reflects the strategic decision that **Yasin-AI is the canonical AI platform**, while distinguishing target integration edges from dependencies already proven in source.
