# ADR-0006: YasinCLI as Ecosystem Control Surface

- Status: Proposed
- Date: 2026-08-09
- Decision owners: Yasin ecosystem maintainers
- Scope: YasinCLI and ecosystem operations
- Supersedes: None
- Superseded by: None

## Context

Yasin needs a unified command-line interface for operating and inspecting multiple ecosystem components. A CLI should simplify control without duplicating the internal implementation of every project.

## Decision

YasinCLI is the unified operator/developer control surface for the Yasin ecosystem. It orchestrates commands against component-owned interfaces but does not become the owner of the underlying Core, Agent, Hub, Relay, Feed, or AI runtime logic.

## Rationale

A dedicated control surface provides a consistent operator experience while preserving component ownership and allowing the underlying projects to evolve independently.

## Alternatives Considered

### Separate CLI for every component only
Rejected as the sole operator experience because it fragments ecosystem operations.

### Move component logic into YasinCLI
Rejected because a control surface should not become a monolithic runtime.

## Consequences

### Positive

- Unified operator experience.
- Centralized status/doctor/start/stop/restart entry points where supported.
- Clear distinction between control and implementation ownership.

### Negative / Trade-offs

- CLI compatibility depends on component contracts.
- A CLI command may need coordinated changes when a component API changes.

### Operational

Commands should report actual component state rather than infer success merely from command execution.

### Security

CLI operations inherit or explicitly establish authorization boundaries; convenience must not bypass component security.

## Architecture Impact

Defines YasinCLI as a control-plane surface over ecosystem components.

## Evidence

- `YASIN_AI_CONTEXT.md`
- `docs/ai/AI_PROJECT_SELECTION_MATRIX.md`
- YasinCLI architecture/project documentation

Exact command-to-component contracts remain subject to source verification.

## Related Documents

- ADR-0001
- ADR-0004

## Open Questions

- Which commands are guaranteed ecosystem-wide contracts?
- How should CLI versioning track component API compatibility?
