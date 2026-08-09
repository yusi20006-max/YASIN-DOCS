# Yasin Ecosystem — Master Architecture

**Document status:** Initial Master Architecture / evidence-based baseline  
**Verified:** 2026-08-09  
**Repository:** `yusi20006-max/YASIN-DOCS`

> This document is the system-level architectural map of the Yasin Ecosystem. It is intentionally conservative: verified implementation facts are separated from conceptual relationships and unresolved questions. Detailed source audits may refine this document.

---

## 1. Purpose

The Yasin Ecosystem is a multi-repository software system. Its repositories should not be treated as isolated applications: they form a set of components with different responsibilities, interfaces, and lifecycle concerns.

The purpose of this document is to give a developer or AI coding agent enough context to answer four questions before changing code:

1. **What is this component responsible for?**
2. **Which component owns the responsibility I am changing?**
3. **What interfaces or dependencies cross the boundary?**
4. **What other repositories can be affected by the change?**

This document is the architectural index. Implementation-level details remain in the owning repositories and their project records in `docs/projects/`.

---

## 2. Architectural Ground Rules

### 2.1 Repository ownership

Every significant capability should have a clear owning project. Convenience is not sufficient reason to duplicate a capability across repositories.

### 2.2 Evidence over assumption

A repository name, README statement, or historical plan is not enough to establish an implemented dependency. Cross-project relationships are promoted to **verified** only when source/configuration/contract evidence supports them.

### 2.3 Current vs planned

Documentation must distinguish:

- **Implemented:** verified in the current repository state.
- **Partial:** evidence exists, but the complete behavior has not been audited.
- **Proposed:** intended architecture, not necessarily implemented.
- **Unknown:** insufficient evidence.

### 2.4 Boundary preservation

A project should not silently absorb another project's responsibilities. Cross-cutting changes require an explicit review of ownership and interface boundaries.

### 2.5 Documentation is not implementation

YASIN-DOCS describes the ecosystem. Runtime/application source code remains in its owning repository.

---

## 3. Ecosystem at a Glance

The currently identified primary ecosystem components are:

```text
                         YASIN ECOSYSTEM
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
          ▼                     ▼                     ▼
     Foundation             AI / Agent          Management /
     & Runtime              Capabilities        Control Plane
          │                     │                     │
          │                     │                     ▼
          │                     │                 YasinHub
          │                     │                 YasinCLI
          │                     │
          ▼                     ▼
      Yasin-Core          Yasin-Agent
                          Yasin-AI
          │                     │
          └──────────┬──────────┘
                     │
                     ▼
             Integration / Data
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
     YasinRelay              YasinFeed
     OpenFeed               YasinPress
     FeedBridge                  │
          │                      │
          └──────────┬───────────┘
                     ▼
              External Platforms

                 YASIN-DOCS
          (architecture / knowledge)
```

**Important:** this diagram is a conceptual layer map, not yet a verified runtime dependency graph. The exact edges will be established by detailed source audits.

---

## 4. Component Classification

### 4.1 Foundation

**Yasin-Core** is currently classified as the ecosystem foundation/runtime component. Its exact public API and verified downstream consumers require detailed source audit.

### 4.2 Agent layer

**Yasin-Agent** is currently classified as the agent platform/runtime component. Its exact boundary with Yasin-Core and Yasin-AI requires source-level verification.

### 4.3 AI layer

**Yasin-AI** is classified as an AI-related ecosystem component. Its exact service/provider boundary is intentionally not assumed until the source audit is complete.

### 4.4 Management / control plane

**YasinHub** is currently evidenced as a management/status component. It must not be treated as a large orchestration system merely because the ecosystem may eventually use it for orchestration.

**YasinCLI** is the ecosystem control-plane/developer tooling project. Its command and API ownership will be documented from the actual implementation.

### 4.5 Integration / transport

**YasinRelay** is classified as the relay/integration layer.

**OpenFeed** is a related Telegram public-channel fetching/API/PWA project.

**FeedBridge** is a related Telegram content bridge/publishing project. Its relationship with YasinRelay/OpenFeed requires careful ownership analysis.

### 4.6 Content applications

**YasinFeed** is classified as a content generation and publishing pipeline.

**YasinPress** is classified as an automated Persian news collection and Eitaa publishing application based on its repository documentation.

These applications should not be assumed to share implementation ownership simply because they process similar content.

### 4.7 Documentation

**YASIN-DOCS** is the ecosystem-level documentation and architectural knowledge repository.

---

## 5. Responsibility Model

The current responsibility model is deliberately high-level:

| Component | Primary responsibility | Explicit caution |
|---|---|---|
| Yasin-Core | Foundation/runtime | Do not infer all shared services without source evidence |
| Yasin-Agent | Agent platform/runtime | Verify exact runtime and Core boundary |
| Yasin-AI | AI component/services | Verify provider and service ownership |
| YasinHub | Management/status | Do not assume full orchestration yet |
| YasinCLI | Control-plane CLI/tooling | Commands/contracts require source audit |
| YasinRelay | Relay/integration | Verify transport ownership |
| OpenFeed | Telegram fetching/API/PWA | Related project; relationship requires audit |
| FeedBridge | Telegram bridge/publishing | Avoid duplicate transport responsibilities |
| YasinFeed | Content generation/publishing | Application boundary must remain explicit |
| YasinPress | News collection/publishing | Treat as separate application until overlap is proven |
| YASIN-DOCS | Ecosystem documentation | Not a runtime dependency |

---

## 6. Dependency Architecture

The **authoritative dependency graph is not yet complete**.

The registry intentionally leaves unverified dependency edges empty. This prevents the master architecture from manufacturing a dependency graph from project names or historical plans.

### Required evidence for a verified dependency

A relationship should be promoted to verified when one or more strong forms of evidence exist, such as:

- direct package/import dependency;
- HTTP/API client integration;
- configuration reference;
- subprocess/CLI invocation;
- documented contract backed by implementation;
- CI/integration test proving the relationship;
- deployment topology proving runtime coupling.

---

## 7. Data Flow Model

At ecosystem level, several classes of data can exist:

```text
External Sources
      │
      ▼
Ingestion / Fetching
      │
      ▼
Normalization / Processing
      │
      ▼
AI Transformation (where applicable)
      │
      ▼
Storage / Queue
      │
      ▼
Publishing / Delivery
      │
      ▼
External Destinations
```

This is a **domain model**, not a claim that every Yasin project implements every stage.

Project-specific pipelines must identify their own ownership of each stage.

---

## 8. Control Flow Model

The ecosystem may contain several control planes:

```text
Developer / Operator
        │
        ▼
     YasinCLI
        │
        ▼
  Management APIs / Services
        │
        ├── Runtime status
        ├── Lifecycle operations
        ├── Diagnostics
        └── Project-specific actions
```

The actual command-to-service relationships remain subject to YasinCLI and YasinHub source audits.

---

## 9. AI Flow

The architectural concept for AI-enabled applications is:

```text
Application / Agent
       │
       ▼
AI abstraction / service boundary
       │
       ▼
Provider / Model
       │
       ▼
Response / structured result
       │
       ▼
Application or Agent
```

The exact implementation of the AI boundary must be derived from Yasin-AI, Yasin-Agent, and consuming projects.

An application should not bypass an established shared AI boundary without an explicit architectural reason.

---

## 10. Agent Flow

Conceptually:

```text
Intent / Task
     │
     ▼
Agent Runtime
     │
     ├── Context / Memory
     ├── Planning / Decision
     ├── Tool Invocation
     ├── External Integration
     └── Result Handling
     │
     ▼
Task Result
```

Yasin-Agent and Yasin-Core must be audited together to establish which portions belong to runtime, foundation, memory, tools, or application layers.

---

## 11. Memory Architecture

Memory is a cross-cutting architectural concern, but no memory dependency is declared here until the current implementation is verified.

Future documentation must distinguish:

- short-lived execution context;
- persistent agent memory;
- application/domain storage;
- cache;
- queue/job state;
- configuration/secrets.

These should not be treated as interchangeable storage mechanisms.

---

## 12. Integration Architecture

Integration boundaries should be explicit for:

- Telegram;
- Eitaa;
- RSS/news sources;
- AI providers;
- GitHub/Jules workflows;
- local/Termux environments;
- external APIs;
- publishing destinations.

The integration layer should own transport-specific behavior where that ownership is architecturally appropriate, while applications retain domain-specific policy.

OpenFeed, FeedBridge, YasinRelay, YasinFeed, and YasinPress require detailed overlap analysis before any consolidation is recommended.

---

## 13. Configuration Architecture

Every project should document:

```text
Configuration source
       │
       ├── defaults
       ├── config files
       ├── environment variables
       └── secrets
```

Secrets must never be represented as ordinary configuration values in source control.

Cross-project configuration contracts must identify:

- variable/key name;
- owner;
- consumer;
- required/optional status;
- format;
- security sensitivity;
- failure behavior.

---

## 14. Security Architecture

At ecosystem level, security boundaries include:

1. credentials and API keys;
2. external service authentication;
3. project-to-project authentication;
4. untrusted external content;
5. AI/provider boundaries;
6. command execution;
7. publishing permissions;
8. local Termux/host permissions;
9. CI/CD secrets.

Security claims require evidence from implementation and deployment configuration.

---

## 15. Deployment / Runtime Model

The ecosystem contains projects that may run in different environments, including local development, Termux, hosted services, CI environments, and application-specific runtimes.

No single deployment topology is declared until each project's runtime model is audited.

The final deployment architecture must distinguish:

- process boundaries;
- service boundaries;
- persistent storage;
- queues/jobs;
- scheduled execution;
- network boundaries;
- secret stores;
- external dependencies.

---

## 16. Testing Architecture

Cross-project quality should include the appropriate combination of:

- unit tests;
- integration tests;
- contract/API tests;
- smoke tests;
- end-to-end tests;
- CI validation;
- compatibility checks.

A project should not claim ecosystem compatibility solely because its local tests pass.

Cross-project contracts should receive explicit integration coverage where practical.

---

## 17. Change Management

Before changing a project:

```text
Read project documentation
        ↓
Inspect current implementation
        ↓
Identify owning responsibility
        ↓
Check PROJECT_REGISTRY
        ↓
Check cross-project consumers
        ↓
Change implementation
        ↓
Run appropriate tests
        ↓
Update affected documentation
        ↓
Record architectural decision if necessary
```

For cross-project changes, inspect both producer and consumer sides of the interface.

---

## 18. AI Coding Agent Operating Model

An AI agent working on Yasin should follow this sequence:

### Step 1 — Establish context

Read:

- `README.md`;
- `ECOSYSTEM.md`;
- `PROJECTS.md`;
- `docs/projects/PROJECT_REGISTRY.yaml`;
- this Master Architecture;
- the target project's repository documentation.

### Step 2 — Verify reality

Inspect the target repository's current branch, source tree, configuration, tests, and interfaces.

### Step 3 — Determine ownership

Do not implement a feature in a project until its architectural owner is clear.

### Step 4 — Check blast radius

Search for consumers, API calls, imports, configuration references, CI dependencies, and documentation references.

### Step 5 — Implement narrowly

Prefer the smallest change that preserves established boundaries.

### Step 6 — Validate

Run relevant tests and checks and inspect the resulting diff.

### Step 7 — Update architecture knowledge

If the change modifies a cross-project contract or architectural boundary, update YASIN-DOCS and create an ADR when appropriate.

---

## 19. Architecture Decision Records

Major decisions should be captured under:

```text
 docs/architecture/decisions/
```

Examples of decisions that should eventually be recorded:

- ecosystem project boundaries;
- Yasin-Core ownership;
- Yasin-Agent/Core boundary;
- Yasin-AI ownership;
- YasinHub control/management scope;
- YasinCLI control-plane scope;
- YasinRelay/OpenFeed/FeedBridge boundaries;
- YasinFeed/YasinPress application boundaries;
- YASIN-DOCS as system-level source of truth.

---

## 20. Known Architectural Questions

The following questions remain intentionally open:

1. What exact public API does Yasin-Core expose today?
2. Which Yasin-Agent capabilities are implemented by Core versus Agent?
3. What exactly is owned by Yasin-AI?
4. Which services does YasinHub actually orchestrate today?
5. What are YasinCLI's current control-plane interfaces?
6. What is the canonical relationship between YasinRelay, OpenFeed, and FeedBridge?
7. Which content-processing capabilities overlap between YasinFeed and YasinPress?
8. Which repositories are production-active versus historical/experimental?
9. What are the actual runtime/deployment topologies?
10. Which APIs are intended to be stable public contracts?
11. Which cross-project tests already exist?
12. Which architectural decisions are already implemented but undocumented?

These questions become inputs to the detailed project audit phase.

---

## 21. Architecture Maturity Model

```text
Level 0 — Unknown
Level 1 — Repository identified
Level 2 — README-level role understood
Level 3 — Source architecture audited
Level 4 — Interfaces/dependencies verified
Level 5 — Cross-project architecture verified
Level 6 — Operational/testing/security model verified
Level 7 — AI-ready documented system
```

The objective of YASIN-DOCS is ultimately **Level 7** for the active ecosystem.

---

## 22. Relationship to Other Documentation

| Document | Purpose |
|---|---|
| `ECOSYSTEM.md` | High-level ecosystem orientation |
| `PROJECTS.md` | Project index |
| `docs/projects/PROJECT_REGISTRY.yaml` | Machine-readable registry |
| `docs/projects/PROJECT_REGISTRY.md` | Human-readable registry |
| `docs/projects/PROJECT_STATUS_MATRIX.md` | Audit coverage |
| `MASTER_ARCHITECTURE.md` | System-level architecture |
| Project records | Per-project implementation architecture |
| ADRs | Decision rationale |
| AI documents | AI-agent operating context |

---

## 23. Completion Criteria

This Master Architecture becomes **production-grade** only after:

- all active repositories receive source-level audits;
- dependencies and consumers are verified;
- stable interfaces are documented;
- data/control/AI/agent flows are backed by implementation evidence;
- deployment and security boundaries are verified;
- important architectural decisions are captured;
- discrepancies between documentation and source are resolved;
- AI handoff documentation can reproduce the ecosystem's architecture without relying on conversation history.

Until then, this document is the **initial evidence-based master architecture baseline**.
