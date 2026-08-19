# ADR-0013: Yasin-MCP as the AI Access / Integration Layer

- Status: Accepted
- Date: 2026-08-19
- Decision owners: Yasin ecosystem maintainers
- Scope: Yasin-MCP and its relationship to the Yasin ecosystem
- Supersedes: None
- Superseded by: None

## Context

The Yasin ecosystem now has distinct ownership boundaries for runtime, agents, AI capabilities, control/observability, operations, documentation, and user-facing CLI workflows. AI agents nevertheless need a standardized way to inspect these boundaries without importing private implementation modules or duplicating project-specific integration logic.

The ecosystem also contains `Yasin-Operations`, which owns optional operational tooling and safety-enforced runtime operations. It must remain independent and must not become an implicit dependency of every integration layer.

A dedicated MCP server can provide a stable AI-facing integration boundary while preserving the existing ownership model.

## Decision

1. Create a standalone repository named `yusi20006-max/Yasin-MCP`.
2. Yasin-MCP is the ecosystem's **AI/agent-facing access and integration layer**.
3. Yasin-MCP does not replace YASIN-DOCS, YasinCLI, YasinHub, Yasin-Operations, Yasin-Core, Yasin-Agent, or Yasin-AI.
4. YASIN-DOCS remains the source of truth for system-level architecture, ADRs, and documented decisions.
5. Yasin-AI remains the canonical owner of ecosystem-wide AI capabilities. Yasin-MCP does not implement model/provider routing, RAG, memory, or other AI platform internals.
6. YasinHub remains the ecosystem control/observability plane. Yasin-MCP must not become a second control plane.
7. YasinCLI remains the human-facing unified interface. Yasin-MCP must not duplicate CLI business logic.
8. Yasin-Operations remains optional and independent. Yasin-MCP may consume its public operational contracts through an adapter where appropriate, but Yasin-MCP must remain runnable without Yasin-Operations.
9. Cross-project integration must use public APIs, SDKs, protocol contracts, or adapters. Private-module imports are prohibited.
10. Phase 1 is strictly read-only.
11. Any future mutating operation must be explicitly typed, permissioned, confirmation-aware, audited, and fail closed.
12. Yasin-MCP is not a mandatory runtime dependency of any existing Yasin project.

## Canonical Role Model

```text
YASIN-DOCS
  = system knowledge / architecture / decisions

Yasin-Core
  = runtime + SDK foundation

Yasin-Agent
  = agent/workflow execution

Yasin-AI
  = canonical AI capability platform

YasinHub
  = control + observability + lifecycle

Yasin-Operations
  = optional operational authority / diagnostics / lifecycle tooling

YasinCLI
  = human-facing unified command interface

Yasin-MCP
  = AI/agent-facing access + integration interface
```

## Initial Integration Model

```text
                         AI Agent / ChatGPT
                                  │
                                  ▼
                           ┌────────────┐
                           │ Yasin-MCP  │
                           └─────┬──────┘
                                 │
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                  ▼
         YASIN-DOCS          GitHub          Public Yasin APIs
              │                  │                  │
              ▼                  ▼                  ▼
         Architecture       Code/PR/Issue     Runtime/Status
         ADR/Contracts       inspection       /capabilities
                                 │                  │
                                 └────────┬─────────┘
                                          ▼
                                  Evidence-aware AI
```

## Phase Boundary

### Phase 1 — Read-Only

Allowed:

- documentation search/read;
- repository and project discovery;
- issue/PR/status inspection;
- capability/version inspection;
- health/diagnostic reads through public contracts;
- architecture/dependency inspection.

Not allowed:

- arbitrary shell execution;
- arbitrary file writes;
- GitHub writes;
- service lifecycle mutation;
- memory mutation/deletion;
- deployment;
- destructive actions.

### Future Controlled Actions

Future write capability requires a separate security decision and must include:

- explicit tool safety class;
- authorization policy;
- confirmation semantics;
- protected-target rules;
- audit/correlation IDs;
- deterministic error model;
- timeout/retry limits;
- dry-run where applicable;
- clear actor/source attribution.

## Alternatives Considered

### Put MCP functionality inside Yasin-Agent
Rejected. Yasin-Agent owns agent/workflow execution, not ecosystem-wide integration access. Embedding MCP there would couple a protocol boundary to one agent runtime and make reuse by other agents harder.

### Put MCP functionality inside YasinHub
Rejected. YasinHub is the control/observability plane. Combining AI access with control-plane ownership would blur authorization and responsibility boundaries.

### Put MCP functionality inside Yasin-Operations
Rejected as the canonical location. Yasin-Operations is an optional operations authority with a safety-enforced execution model. MCP access can consume its public contracts but should not make the operations layer the owner of all AI-facing integration.

### Add MCP support to YasinCLI only
Rejected. CLI is the human-facing command surface and should not become the protocol implementation for external AI agents.

## Consequences

### Positive

- A single AI-facing integration boundary can serve multiple agents and clients.
- Private cross-repository coupling is reduced.
- Read-only inspection can be standardized before any write capability is introduced.
- Architecture drift can later be detected by combining YASIN-DOCS, GitHub, and runtime evidence.
- Yasin-Operations can remain optional while exposing useful operational information through a controlled adapter.

### Negative / Costs

- A new repository and compatibility surface must be maintained.
- Tool/resource contracts require explicit versioning and governance.
- Security and authorization become first-class concerns before write operations can be enabled.
- Adapters must handle unavailable projects gracefully.

## Evidence Policy

Yasin-MCP is an accepted architectural decision but remains a new implementation target. It must not be represented as an implemented dependency until source-level evidence exists.

## Related Documents

- `docs/architecture/YASIN_ECOSYSTEM_CANONICAL_ARCHITECTURE_V1.md`
- `docs/architecture/ECOSYSTEM_DEPENDENCY_MATRIX_V1.md`
- `docs/architecture/YASIN_MCP_ARCHITECTURE_V1.md`
- `docs/adr/ADR-0012-yasin-operations-boundary.md`
- `docs/adr/ADR-001-YASIN-AI-CANONICAL-AI-PLATFORM.md`
- `docs/projects/PROJECT_REGISTRY.md`
