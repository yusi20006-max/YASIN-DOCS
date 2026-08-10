# Yasin Ecosystem — API & Contract Registry v1

## Purpose

This document defines the canonical registry for **cross-project interfaces and contracts** in the Yasin ecosystem.

It distinguishes:

- confirmed interfaces supported by repository evidence;
- inferred integration boundaries;
- proposed future contracts;
- unresolved interfaces requiring further audit.

It does **not** invent payload schemas where source evidence is unavailable.

---

## 1. Contract Model

Every ecosystem contract should eventually specify:

| Field | Meaning |
|---|---|
| Contract ID | Stable identifier |
| Owner | Project responsible for defining and maintaining it |
| Consumer | Project(s) using it |
| Direction | Producer → consumer |
| Transport | Python API, SDK, CLI, HTTP, process, file, event, etc. |
| Schema | Request/response or message shape |
| Version | Contract version |
| Errors | Failure semantics |
| Auth | Authentication/authorization requirements |
| Compatibility | Backward/forward compatibility rules |
| Status | Confirmed / Inferred / Proposed / Unresolved |

Until these fields are established by implementation or an ADR, the contract remains incomplete.

## 2. Contract Registry

| ID | Producer | Consumer | Boundary | Status |
|---|---|---|---|---|
| CORE-SDK | Yasin-Core | Yasin-Agent, YasinHub, YasinCLI | Python SDK/public API | Confirmed baseline |
| AGENT-SDK | Yasin-Agent | YasinHub, YasinCLI | Agent SDK/public API | Confirmed baseline |
| HUB-CONTROL | YasinHub | YasinCLI / operators | Control/operational interface | Confirmed baseline; schema normalization pending |
| RELAY-ADAPTER | YasinRelay | YasinCLI / Hub | Operational adapter | Confirmed baseline |
| RELAY-AI-PROCESSOR | YasinRelay | AI provider implementations | Internal provider abstraction | Confirmed baseline |
| FEED-PUBLISHER | YasinFeed | Publishing providers | Application adapter | Confirmed baseline |
| PRESS-AI | YasinPress | Cloudflare Workers AI | Optional provider integration | Confirmed baseline |
| AI-PLATFORM | Yasin-AI | Future consumers | AI platform API | Platform exists; cross-project contract unresolved |
| CLI-ECOSYSTEM | YasinCLI | Ecosystem projects | Unified orchestration | Partially confirmed |

## 3. Core SDK Contract

### Contract ID

`CORE-SDK`

### Owner

Yasin-Core

### Consumers

- Yasin-Agent
- YasinHub
- potentially YasinCLI through an adapter

### Purpose

Expose stable reusable runtime/SDK capabilities without coupling Core to higher-level applications.

### Boundary rule

```text
Yasin-Core
   ↑
Agent / Hub / other consumers
```

Core must not depend on Hub, Feed, Press, Relay, or application-specific orchestration.

### Status

**Confirmed baseline.** Exact public symbols and signatures belong in the Core-specific API document and must be verified against source before being declared stable.

## 4. Agent SDK Contract

### Contract ID

`AGENT-SDK`

### Owner

Yasin-Agent

### Consumers

- YasinHub
- YasinCLI through an adapter

### Purpose

Expose agent/workflow execution capabilities to operational tooling without requiring consumers to import Agent internals.

### Status

**Confirmed baseline.** Exact method signatures and lifecycle semantics require source-level API inventory.

## 5. Hub Control Contract

### Contract ID

`HUB-CONTROL`

### Owner

YasinHub

### Consumers

- YasinCLI
- human operators
- ecosystem automation

### Purpose

Provide ecosystem-level lifecycle and observability operations such as status, health, start/stop/restart/doctor-style functionality.

### Architectural rule

Hub is the control plane. A project may expose its own runtime interface, while Hub orchestrates it through a public boundary.

### Important distinction

```text
YasinCLI → Hub control interface
```

is an operational relationship, not permission for CLI to duplicate Hub's internal implementation.

### Status

**Confirmed baseline; schema normalization pending.**

## 6. Relay AIProcessor Contract

### Contract ID

`RELAY-AI-PROCESSOR`

### Owner

YasinRelay

### Consumers

AI provider implementations used by Relay.

### Purpose

Decouple the Relay processing pipeline from a specific AI provider.

### Conceptual flow

```text
Relay Pipeline
      ↓
 AIProcessor
      ↓
Provider implementation
```

This contract must not be described as a direct dependency on Yasin-AI unless a dedicated integration adapter is introduced.

### Status

**Confirmed baseline.**

## 7. Feed Publisher Contract

### Contract ID

`FEED-PUBLISHER`

### Owner

YasinFeed

### Consumers

Publishing destinations such as RSS/PWA/Eitaa adapters.

### Purpose

Keep content generation and transformation independent from destination-specific publishing behavior.

### Status

**Confirmed baseline.** Exact destination payload schemas belong to Feed's API documentation.

## 8. Press AI Provider Contract

### Contract ID

`PRESS-AI`

### Owner

YasinPress

### Provider

Cloudflare Workers AI (optional integration).

### Purpose

Perform optional AI-assisted processing in the Press pipeline without making the whole application dependent on AI availability.

### Status

**Confirmed baseline.** Provider-specific request/response schema must be maintained with implementation evidence.

## 9. Yasin-AI Platform Contract

### Contract ID

`AI-PLATFORM`

### Owner

Yasin-AI

### Potential Consumers

- Yasin-Agent
- YasinHub
- YasinFeed
- YasinPress
- YasinRelay
- external applications

### Current status

The Yasin-AI platform exists, but the canonical cross-project integration contract is **unresolved**.

Therefore the following must not be assumed:

```text
Feed → Yasin-AI
Press → Yasin-AI
Relay → Yasin-AI
Agent → Yasin-AI
Core → Yasin-AI
```

A future AI integration must define authentication, request/response schema, provider selection, failure handling, timeout, retry, rate limiting, and compatibility.

## 10. YasinCLI Ecosystem Contract

### Contract ID

`CLI-ECOSYSTEM`

### Owner

YasinCLI

### Purpose

Present one user-facing command surface over ecosystem services.

### Current boundary

The architecture baseline identifies first-class adapter coverage for:

```text
Core
Agent
Hub
Relay
```

Feed, Press, and AI are not to be treated as fully integrated until source evidence confirms their adapters.

### Rule

CLI should orchestrate through public contracts and adapters, not copy internal project logic.

## 11. Contract Direction Rules

### Allowed

```text
Application → public platform SDK
Hub → public project SDK/API
CLI → public adapter/API
Agent → Core
```

### Not allowed without explicit architecture decision

```text
Core → Hub
Core → Feed/Press/Relay
Project → Hub internal modules
CLI → private project implementation
Shared database → implicit integration
```

## 12. Transport Registry

Current confirmed transport categories:

| Contract family | Transport category | Status |
|---|---|---|
| Core SDK | Python API/SDK | Confirmed |
| Agent SDK | Python API/SDK | Confirmed |
| Hub control | CLI/process/public service boundary | Confirmed baseline |
| Relay AIProcessor | In-process abstraction | Confirmed |
| Feed publishers | Application adapter interfaces | Confirmed |
| Press AI | Provider API | Confirmed |
| AI platform | Service/API boundary | Existing platform; ecosystem contract unresolved |

Exact wire-level schemas are intentionally deferred until source-level contract extraction.

## 13. Error & Reliability Contract

Every production cross-project contract should eventually define:

- timeout;
- retry policy;
- idempotency;
- error categories;
- partial failure behavior;
- health reporting;
- circuit breaking where relevant;
- rate limits;
- observability fields.

If these are not implemented or documented, the contract must remain marked incomplete rather than assumed.

## 14. Authentication & Trust

Contract owners must define the trust model for service boundaries.

Current architecture principle:

```text
Local SDK
 → local process trust boundary

Remote API
 → explicit authentication required

Provider integration
 → provider credential owned by consuming application
```

Secrets must not be moved into a shared global configuration simply because projects are documented together.

## 15. Versioning Rules

Contract versions must be independent from repository versions when necessary.

Recommended notation:

```text
CORE-SDK v1
AGENT-SDK v1
HUB-CONTROL v1
RELAY-AI-PROCESSOR v1
```

Breaking changes require:

1. contract version increment;
2. compatibility assessment;
3. migration documentation;
4. affected project audit;
5. ADR when the ecosystem boundary changes.

## 16. Contract Ownership Rule

The producer owns the contract definition.

```text
Producer
   ↓ owns schema
Consumer
   ↓ implements client
```

A consumer may request changes, but should not silently redefine the producer's contract.

## 17. AI Agent Rules for Contracts

Before adding an integration, an AI coding agent must:

1. search this registry;
2. determine whether an existing contract already covers the need;
3. inspect producer source and tests;
4. identify the contract owner;
5. avoid private/internal imports across repositories;
6. define schema and failure semantics before introducing a new service boundary;
7. update this registry;
8. add/update an ADR for a new cross-project architectural dependency;
9. update the compatibility matrix if versions become coupled.

## 18. Contract Lifecycle

```text
Idea
 ↓
Proposed
 ↓
ADR / Design
 ↓
Implementation
 ↓
Source + Tests
 ↓
Confirmed
 ↓
Versioned
 ↓
Deprecated
 ↓
Removed
```

## 19. Open Contract Work

The next source-audit tasks are:

1. extract exact Core public API symbols;
2. extract exact Agent SDK symbols;
3. inventory Hub control commands/API;
4. inventory YasinCLI adapter interfaces;
5. inventory Relay `AIProcessor` methods;
6. inventory Feed publisher interfaces;
7. inventory Press provider contract;
8. determine whether Yasin-AI has a stable external API suitable for ecosystem consumption;
9. build request/response schemas;
10. define compatibility guarantees.

## 20. Status

**API & Contract Registry v1 established.**

The registry intentionally records the architecture without fabricating wire schemas. Exact API extraction is the next implementation-backed step of the contract phase.
