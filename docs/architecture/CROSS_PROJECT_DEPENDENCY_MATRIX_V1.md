# Yasin Ecosystem — Cross-Project Dependency Matrix v1

## Purpose

This document consolidates the completed ecosystem audits and separates confirmed dependencies from documented boundaries and planned integrations.

## Evidence Classes

```text
VERIFIED        Concrete source/import/API evidence exists.
DOCUMENTED      Repository documentation explicitly describes the boundary.
PLANNED         Architecture/roadmap intent only.
NOT CONFIRMED   Evidence is insufficient to claim a dependency.
```

## 1. Canonical Dependency Matrix

| Consumer | Provider / Dependency | Status | Evidence |
|---|---|---|---|
| Yasin-Agent | Yasin-Core SDK | VERIFIED | YasinCoreClient / Core SDK integration |
| YasinHub | Yasin-Core SDK | VERIFIED | YasinCoreClient / compatibility API |
| YasinRelay | Yasin-Core | NOT CONFIRMED | Own pipeline/provider boundaries |
| YasinFeed | Yasin-AI | NOT CONFIRMED | AI/rewrite boundary exists, provider not established |
| YasinPress | Cloudflare Workers AI | DOCUMENTED | ai_engine provider documented |
| YasinPress | Yasin-AI | NOT CONFIRMED | No explicit adapter/source dependency established |
| YasinCLI | Yasin-Core | PLANNED | Unified control contract; implementation baseline incomplete |
| YasinCLI | Yasin-Agent | PLANNED | Adapter boundary planned |
| YasinCLI | YasinHub | PLANNED | Adapter boundary planned |
| YasinCLI | YasinRelay | PLANNED | Adapter boundary planned |
| Yasin-AI | Yasin-Core | NOT CONFIRMED | Independent platform boundary |
| YasinHub | Yasin-Agent | NOT CONFIRMED | Registry/control knowledge is not dependency evidence |
| YasinHub | YasinRelay | NOT CONFIRMED | Registry/control knowledge is not dependency evidence |

## 2. Confirmed Core Integration Paths

```text
Yasin-Agent
    ↓
YasinCoreClient / SDK
    ↓
Yasin-Core Runtime
```

Status: **VERIFIED**.

```text
YasinHub
    ↓
YasinCoreClient
    ↓
Yasin-Core
```

Status: **VERIFIED**.

## 3. Provider Boundaries

YasinRelay exposes a provider-neutral `ContentProcessor` / `AIProcessor` boundary. This confirms an AI-provider integration point, but does not establish a direct Yasin-AI dependency.

YasinPress documents Cloudflare Workers AI as its optional provider. This does not establish a Yasin-AI dependency.

YasinFeed has an AI/rewrite responsibility, but the audited evidence is insufficient to identify Yasin-AI as its concrete backend.

## 4. Control Plane vs Runtime Plane

```text
                 CONTROL PLANE
                     │
                  YasinHub
                     │
                  YasinCLI
                     │
                     ▼
                RUNTIME PLANE
                     │
                 Yasin-Core
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Agent       Tasks      Services
```

Content applications remain separate:

```text
YasinFeed
YasinPress
YasinRelay
```

They should consume explicit interfaces rather than control-plane internals.

## 5. Memory / State Ownership

| State | Owner | Shared by default? |
|---|---|---|
| Core runtime memory | Yasin-Core | No |
| Agent session/context | Yasin-Agent | No |
| AI platform memory | Yasin-AI | No |
| Hub operational status | YasinHub | No |
| Feed storage | YasinFeed | No |
| Press database/queue | YasinPress | No |
| Relay database/pipeline state | YasinRelay | No |

**Rule:** local persistence must not silently become shared ecosystem memory.

## 6. Registry vs Dependency Rule

```text
Project Registry Entry
        ≠
Runtime Dependency
```

A dependency becomes `VERIFIED` only when there is direct source use, an explicit SDK/service client, a concrete adapter, or an executable integration test proving the boundary.

A README diagram or registry entry alone is insufficient.

## 7. Dependency Direction Rules

Allowed:

```text
Application
    ↓
Public SDK / API
    ↓
Platform
```

Discouraged:

```text
Application
    ↓
Private implementation module
```

Forbidden without ADR:

```text
Core
  ↓
Application-specific implementation
```

## 8. Compatibility Ownership

Yasin-Core owns the ecosystem compatibility mechanism. Source-verified validators include:

```text
AgentCompatibilityValidator
HubCompatibilityValidator
RelayCompatibilityValidator
CLICompatibilityValidator
RuntimeCompatibilityChecker
```

Project repositories should therefore use the Core compatibility contract rather than inventing incompatible version rules.

## 9. Remaining Verification Work

```text
1. Deep Yasin-Agent integration signatures
2. Deep YasinHub adapters
3. Deep YasinRelay publisher/storage contracts
4. Deep YasinFeed implementation symbols
5. Deep YasinPress implementation symbols
6. Yasin-AI exact service/API symbols
7. YasinCLI repository/source baseline
8. Cross-project integration tests
9. Contract compatibility test suite
10. Final Contract Registry + ADR index
```

## Status

**Cross-Project Dependency Matrix v1 — consolidated baseline complete.**

The matrix intentionally prefers `NOT CONFIRMED` over speculative dependencies.
