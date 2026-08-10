# YasinCLI — Unified Ecosystem Control Contract v1

## Evidence

This audit attempted to locate a dedicated `YasinCLI` repository and source-level implementation. The connected GitHub repository search did not return a repository named `YasinCLI`, and the expected repository path could not be fetched.

Therefore this document is an **architecture contract baseline**, not a source-verified API inventory. No CLI symbol, implementation, argument schema, or exit code is claimed as source-verified.

## 1. Role

YasinCLI is the planned unified command-line control surface for:

```text
Yasin-Core
Yasin-Agent
YasinHub
YasinRelay
```

It is an orchestration layer and must consume public project contracts rather than private implementation modules.

## 2. Planned Core Commands

```text
status
doctor
start
stop
restart
```

These are planned command contracts, not source-verified implementations.

### status

Aggregate ecosystem/service status for Core, Agent, Hub, and Relay.

### doctor

Diagnose configuration, connectivity, dependency, and runtime problems. It should be diagnostic-first and non-destructive by default.

### start / stop / restart

Request lifecycle operations for selected ecosystem services while preserving lifecycle ownership inside each project.

## 3. Adapter Boundary

```text
                  YasinCLI
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
      Core         Agent         Hub
        │            │            │
        └────────────┴────────────┘
                     │
                   Relay
```

The intended architecture uses narrow project adapters. Names such as `CoreAdapter`, `AgentAdapter`, `HubAdapter`, and `RelayAdapter` are placeholders until an implementation exists.

## 4. Contract Principles

1. YasinCLI is orchestration, not a replacement runtime.
2. Project ownership remains with individual repositories.
3. CLI commands consume public APIs/contracts.
4. Private cross-project imports require explicit architectural justification.
5. Lifecycle operations must be explicit and observable.
6. `doctor` must not silently mutate state.
7. `status` must be safe and repeatable.
8. Cross-project contract changes update the central Contract Registry.

## 5. Status Aggregation

Intended flow:

```text
YasinCLI
   ↓
collect status
   ├── Yasin-Core
   ├── Yasin-Agent
   ├── YasinHub
   └── YasinRelay
   ↓
normalized result
```

The future normalized status should distinguish at least:

```text
healthy
running
stopped
degraded
unavailable
unknown
```

Exact values remain open until implementation and tests exist.

## 6. Lifecycle Ownership

```text
CLI request
    ↓
Project adapter
    ↓
Project-owned lifecycle API/command
    ↓
Result
    ↓
CLI normalization
```

YasinCLI must not directly manipulate another project's internal database, state files, or private runtime objects merely to implement lifecycle commands.

## 7. Error Contract

The future CLI contract should distinguish:

```text
invalid command
invalid target
configuration error
dependency unavailable
service unavailable
operation failed
partial failure
```

Exit codes remain open until implementation and test evidence exists.

## 8. Configuration Boundary

YasinCLI may own ecosystem-level targets and locations, but must not become a second source of truth for:

```text
Core configuration
Agent configuration
Hub registry
Relay provider configuration
```

## 9. YasinHub Relationship

YasinHub already has a concrete control/diagnostic surface. YasinCLI should reuse the Hub public/control contract where appropriate rather than duplicating Hub internals.

```text
YasinCLI
   ↓
YasinHub public/control contract
   ↓
Hub-owned operations
```

Direct project adapters remain possible where Hub does not own an operation.

## 10. Contract Status

```text
CLI role                       Architecture verified
Core orchestration             Architecture verified
Agent orchestration            Architecture verified
Hub integration                Architecture verified
Relay integration              Architecture verified
Command names                  Planned baseline
Exact implementation           OPEN
Argument schemas               OPEN
Exit codes                     OPEN
Adapter symbols                OPEN
```

## 11. Source Audit Gate

Before declaring YasinCLI source-verified, the dedicated repository should expose and test:

```text
CLI entrypoint
command registry
adapter modules
configuration model
status model
error/exit-code definitions
integration tests
```

## 12. AI Agent Rules

- Treat this document as a contract baseline, not existing implementation.
- Do not invent APIs for Core, Agent, Hub, or Relay.
- Prefer the existing public contracts of those projects.
- Keep orchestration separate from business logic.
- Add integration tests for every adapter.
- Standardize output schemas and exit codes only with implementation evidence.
- Update the central Contract Registry when adapters become real.
- Use an ADR for new direct cross-project dependencies.

## Status

**YasinCLI Unified Ecosystem Control Contract v1 — architecture baseline established; source-level audit is blocked until the dedicated repository/source is available.**
