# Yasin-MCP Architecture v1

- Status: Target architecture
- Decision: ADR-0013
- Date: 2026-08-19
- Implementation repository: `yusi20006-max/Yasin-MCP`

## 1. Mission

Yasin-MCP is the AI/agent-facing access and integration layer for the Yasin ecosystem.

It exposes bounded MCP tools and resources that let AI agents inspect ecosystem documentation, repositories, public project contracts, status, capabilities, and diagnostics without importing private implementation modules.

## 2. Ownership Boundary

```text
YASIN-DOCS       → system architecture, ADRs, specifications, decisions
Yasin-Core       → runtime + SDK foundation
Yasin-Agent      → agent/workflow execution
Yasin-AI         → canonical AI capability platform
YasinHub         → control + observability + lifecycle
Yasin-Operations → optional operational authority
YasinCLI         → human-facing unified CLI
Yasin-MCP        → AI/agent-facing access + integration
```

Yasin-MCP owns protocol exposure and adapter composition. It does not take ownership of the underlying domain logic.

## 3. Layer Model

```text
                     AI CLIENTS
              ChatGPT / Agents / Codex / Other
                           │
                           ▼
                    ┌─────────────┐
                    │  Yasin-MCP  │
                    │ MCP Server  │
                    └──────┬──────┘
                           │
          ┌────────────────┼─────────────────┐
          ▼                ▼                 ▼
      Resources          Tools           Capability
          │                │              Discovery
          ▼                ▼                 │
   Docs / Contracts   Read Adapters          │
   Project Context    Public APIs             │
          │                │                 │
          └────────────────┼─────────────────┘
                           ▼
                 Yasin ecosystem boundaries
```

## 4. Core Modules

```text
src/yasin_mcp/
├── server/        MCP lifecycle and transport boundary
├── protocol/      Tool/resource schemas and protocol models
├── capabilities/  Capability discovery and version negotiation
├── tools/         Bounded tool definitions
├── resources/     Read-only resource definitions
├── adapters/      GitHub, Docs, Project, Runtime adapters
├── policies/      Authorization/safety policy boundary
├── errors/        Stable machine-readable error model
├── audit/         Audit/correlation hooks for future actions
└── config/        Configuration and environment handling
```

## 5. Adapter Rule

Adapters may call:

- public HTTP/API interfaces;
- public SDKs;
- stable command interfaces where explicitly approved;
- YASIN-DOCS repository content;
- GitHub APIs through a bounded integration.

Adapters must not import private implementation modules from other Yasin repositories.

## 6. Initial Tool Taxonomy

### Ecosystem

```text
list_projects
get_project
get_ecosystem_status
get_dependency_summary
```

### Documentation

```text
search_docs
get_doc
get_adr
get_project_architecture
```

### GitHub

```text
list_repositories
get_repository
search_code
get_issue
list_issues
get_pull_request
list_pull_requests
get_ci_status
```

### Runtime / Diagnostics

```text
get_runtime_status
get_project_health
get_capabilities
get_diagnostics
```

The exact tool contract is implementation work and must be versioned before publication.

## 7. Resources vs Tools

Use **resources** for stable/read-oriented contextual material such as:

- architecture documents;
- project metadata;
- public contracts;
- capability descriptions.

Use **tools** for parameterized operations such as:

- search;
- filtering;
- status queries;
- repository inspection;
- diagnostics.

Mutation must never be hidden behind a resource.

## 8. Evidence Model

Responses should preserve source/evidence state where practical:

- Confirmed — backed by implementation/source evidence.
- Target — selected architecture not yet fully implemented.
- Proposed — candidate design.
- Unresolved — requires a decision or evidence.

Yasin-MCP must not turn a target architecture into a claim of runtime implementation.

## 9. Security Model

Phase 1 is read-only.

Future mutating tools require:

```text
Request
  ↓
Capability check
  ↓
Authorization
  ↓
Safety policy
  ↓
Confirmation (where required)
  ↓
Execution
  ↓
Audit record
  ↓
Structured result
```

The default policy is deny-by-default for mutations.

## 10. Dependency Direction

```text
AI Client
   ↓
Yasin-MCP
   ↓
Public adapters/contracts
   ↓
Yasin ecosystem projects
```

No existing Yasin project should require Yasin-MCP merely because it is available.

The preferred future direction for Yasin-Agent or other agents is consumption of Yasin-MCP as an optional tool/integration surface, not a runtime dependency of their core.

## 11. Yasin-Operations Relationship

Yasin-Operations remains the optional operational authority for safety-enforced lifecycle/diagnostic operations.

Yasin-MCP may expose read-only operational information through a Yasin-Operations adapter when its public contract is stable.

```text
Yasin-MCP
    │
    ▼
Yasin-Operations public contract
    │
    ▼
Operations / Diagnostics
```

Yasin-MCP must continue to operate if Yasin-Operations is absent.

## 12. Yasin-AI Relationship

Yasin-MCP does not become the AI platform.

Yasin-AI remains responsible for:

- model/provider routing;
- inference services;
- knowledge/RAG;
- embeddings;
- durable AI memory;
- AI extensions;
- AI API/SDK contracts.

Yasin-MCP may inspect and expose those public capabilities to AI clients.

## 13. YasinCLI Relationship

```text
Human → YasinCLI → public APIs/adapters
AI    → Yasin-MCP → public APIs/adapters
```

Both are interface layers. Neither should duplicate the internal business logic of the projects they control or inspect.

## 14. Phase Plan

### Phase 0 — Architecture & Contracts

- ADR-0013
- tool/resource taxonomy
- capability/version model
- error model
- security boundary
- adapter rules
- compatibility policy

### Phase 1 — Read-Only Foundation

- MCP server bootstrap
- capability discovery
- Docs adapter
- GitHub read adapter
- project metadata/status adapter
- initial runtime/diagnostic adapter contracts
- unit/integration tests
- CI
- typing/linting/security checks

### Phase 2 — Runtime Integration

- Yasin-Core public contract adapter
- Yasin-Agent public contract adapter
- Yasin-AI public contract adapter
- YasinHub public contract adapter
- optional Yasin-Operations adapter

### Phase 3 — Intelligence

- architecture audit
- dependency analysis
- architecture drift detection
- evidence-aware reports
- cross-repository consistency checks

### Phase 4 — Controlled Actions

- explicit mutating tool contracts
- permission model
- confirmation flow
- audit trail
- dry-run
- protected targets
- deterministic failure/rollback semantics

### Phase 5 — Production AI Control Interface

- production transport/authentication
- capability negotiation
- observability
- compatibility matrix
- performance/resource controls
- end-to-end client verification

## 15. Non-Goals

Yasin-MCP will not:

- become a monolithic replacement for YasinHub;
- become the canonical AI platform;
- replace YASIN-DOCS;
- replace YasinCLI;
- own application business logic;
- expose unrestricted shell access;
- create implicit shared-database coupling;
- make optional projects mandatory dependencies.
