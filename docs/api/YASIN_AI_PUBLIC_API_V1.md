# Yasin-AI — Platform & Public API Contract v1

## Evidence

Source/documentation audit against `yusi20006-max/Yasin-AI` README and `docs/ARCHITECTURE.md`.

Current production release documented by the repository: **v1.1.0**.

The repository has completed its initial architecture and production-hardening cycle, but this audit pass did not produce reliable exact Python symbol matches from repository code search. Therefore this document records the **source-backed platform boundaries** without inventing class or function names.

## 1. Role in the Yasin Ecosystem

Yasin-AI is an independent AI platform providing reusable AI-oriented runtime services, persistent memory, knowledge/retrieval capabilities, developer extensions, API/service boundaries, and observability.

It is a **platform/provider**, not the ecosystem control plane.

Conceptually:

```text
Yasin-AI
├── Runtime Platform
├── API / Service Layer
├── Knowledge Platform
├── Memory Platform
├── Developer / Plugin Platform
├── Observability
└── Deployment / Infrastructure
```

## 2. Architecture Boundary

The repository defines a layered architecture:

```text
Clients / Operators
        ↓
API / CLI / SDK
        ↓
API Service Layer
        ↓
Runtime / Developer Platform
        ↓
Knowledge / Memory
        ↓
Persistence
```

Observability is cross-cutting and deployment/infrastructure remains below the application boundary.

The architecture explicitly requires runtime behavior to remain independent from transports, persistence backends, observability exporters, and deployment tooling. fileciteturn190file0

## 3. Runtime Contract

### Contract ID

`AI-RUNTIME`

### Owner

Yasin-AI

### Responsibility

Own lifecycle and module orchestration for the AI platform.

### Architectural constraints

Runtime core must not depend directly on:

```text
HTTP framework
specific deployment tooling
vendor-specific persistence
monitoring vendor
```

Those concerns belong behind replaceable boundaries.

### Status

**Architecture/source documented; exact symbol API open.**

## 4. API / Service Contract

### Contract ID

`AI-SERVICE`

### Responsibility

Provide transport-neutral request dispatch and response/error contracts.

The architecture explicitly separates:

```text
Transport
   ↓
API Service Layer
   ↓
Core business logic
```

HTTP or another network transport should adapt into the service layer rather than become part of the core business logic. fileciteturn190file0

### Ecosystem implication

Other Yasin projects should consume a stable service/SDK boundary rather than importing Yasin-AI internals.

### Status

**Architecture verified; exact wire schema open.**

## 5. Knowledge Platform Contract

### Contract ID

`AI-KNOWLEDGE`

### Responsibilities

The repository identifies:

```text
retrieval
embeddings
knowledge-oriented components
semantic indexes
```

and graph/reasoning primitives as part of the Knowledge Platform.

This layer should remain independent from any one transport or deployment environment.

### Status

**Architecture verified; exact public symbols open.**

## 6. Memory Platform Contract

### Contract ID

`AI-MEMORY`

### Responsibilities

The Memory Platform owns durable long-term memory abstractions and storage.

Default persistence is:

```text
SQLite
```

with configurable storage paths.

Business logic is expected to interact through storage interfaces/manager abstractions rather than embedding database-specific behavior throughout the application. fileciteturn190file0

### Critical ecosystem distinction

Yasin-AI memory is **platform-owned AI memory**.

It must not automatically be treated as:

```text
Yasin-Core memory
Yasin-Agent session state
YasinHub operational status
YasinFeed storage
YasinPress storage
YasinRelay storage
```

Cross-project sharing requires an explicit integration contract.

## 7. Developer / Plugin Contract

### Contract ID

`AI-PLUGIN`

### Responsibility

Expose narrow extension/plugin interfaces without forcing global registration.

Current security boundary:

```text
Plugin execution = trusted + in-process
```

Untrusted remote plugin execution is explicitly **not supported** in the current release and requires a future sandbox/authorization layer. fileciteturn189file0

### Architectural rule

No ecosystem component should assume that Yasin-AI can safely execute arbitrary untrusted remote plugin code.

## 8. Observability Contract

### Contract ID

`AI-OBSERVABILITY`

Yasin-AI provides dependency-light counters, timers, runtime instrumentation primitives, and performance/reliability regression coverage.

Observability must remain vendor-neutral.

The core platform should not become coupled to a specific monitoring provider merely to expose metrics.

## 9. Persistence Contract

### Contract ID

`AI-PERSISTENCE`

Default:

```text
SQLite-backed local persistence
```

Current documented limitations:

```text
No distributed/high-availability storage claim
No automatic multi-node failover
```

These are intentional current boundaries, not missing documentation. fileciteturn189file0

## 10. Deployment Contract

### Contract ID

`AI-DEPLOYMENT`

Production deployment is containerized and documents:

```text
non-root execution
reduced Linux capabilities
no-new-privileges
read-only root filesystem where supported
separate writable data volume
```

Deployment configuration must remain below the application/service boundary.

## 11. Cross-Project Integration Contract

### Ecosystem Contract ID

`AI-PLATFORM`

Potential consumers include:

```text
Yasin-Agent
YasinHub
YasinFeed
YasinPress
YasinRelay
YasinCLI
```

However, **potential consumer ≠ confirmed dependency**.

Current evidence confirms Yasin-AI as an independent platform, but does not establish direct source-level dependencies from every listed project.

Therefore the canonical rule is:

```text
Project → Yasin-AI
```

must only be added to the dependency graph after a concrete API/SDK/service integration is verified.

## 12. Provider vs Platform Distinction

Yasin-AI may itself use AI models/providers, but its ecosystem role is broader than a single model provider.

Similarly:

```text
YasinPress → Cloudflare Workers AI
```

does not imply:

```text
YasinPress → Yasin-AI
```

unless an explicit adapter is introduced.

## 13. Versioning

Current production release:

```text
Yasin-AI v1.1.0
```

The repository follows semantic versioning:

```text
Patch → backward-compatible fixes
Minor → backward-compatible features
Major → breaking changes
```

Release tags are immutable. fileciteturn189file0

For ecosystem contracts, the platform version and individual API contract version should remain conceptually separate.

## 14. Security Rules for Integrators

Integrators must:

1. treat secrets as runtime configuration;
2. never commit credentials into application state;
3. not assume remote plugin execution is sandboxed;
4. use explicit service/API boundaries;
5. respect the current local SQLite availability model;
6. not assume distributed failover exists;
7. avoid importing deployment-specific implementation into application logic.

## 15. AI Agent Rules

When modifying or integrating Yasin-AI:

1. Start from `docs/ARCHITECTURE.md` and this contract.
2. Prefer narrow service/SDK boundaries.
3. Do not couple consumers to private implementation modules.
4. Keep persistence replaceable.
5. Keep transport separate from core business logic.
6. Treat plugin execution as trusted in-process execution unless/until a sandbox contract is implemented.
7. Do not claim high availability or multi-node failover.
8. Record new ecosystem integrations in the central Contract Registry.
9. Use an ADR for architectural boundary changes.
10. Verify exact public symbols from source before documenting them as stable APIs.

## 16. Open Source-Level API Work

The next deep audit should identify exact symbols and schemas under the implementation directories for:

```text
runtime
API/service layer
knowledge
memory
plugins/extensions
observability
CLI
configuration
```

Required extraction:

- public classes/functions;
- package exports;
- constructor/method signatures;
- request models;
- response models;
- error types;
- plugin lifecycle;
- persistence interfaces;
- service dispatch behavior;
- CLI command contract.

## Status

**Yasin-AI Platform & Public API Contract v1 — architecture/source baseline complete; exact symbol-level API extraction remains open.**
