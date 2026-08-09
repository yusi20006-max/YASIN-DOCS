# ADR-0004: YasinHub Management Boundary

- Status: Proposed
- Date: 2026-08-09
- Decision owners: Yasin ecosystem maintainers
- Scope: YasinHub and ecosystem management
- Supersedes: None
- Superseded by: None

## Context

The ecosystem needs a management/control layer capable of presenting project state and coordinating operational views without absorbing the runtime responsibilities of every component.

## Decision

YasinHub is the primary ecosystem management and status boundary. It should coordinate management concerns and expose ecosystem state without becoming the owner of Core runtime, Agent execution, Relay processing, Feed publishing, or other component-specific business logic.

## Rationale

A dedicated management boundary prevents the control plane from becoming a monolithic implementation layer and allows operational tooling to evolve independently from runtime components.

## Alternatives Considered

### Put management logic into Yasin-Core
Rejected because Core should remain foundational.

### Make YasinHub a universal execution engine
Rejected because execution ownership belongs to the relevant runtime/application component.

## Consequences

### Positive

- Clear control-plane boundary.
- Centralized management views.
- Reduced duplication of runtime ownership.

### Negative / Trade-offs

- Hub must integrate with multiple component contracts.
- Management state can become stale if component status contracts are weak.

### Operational

Status should identify its source and freshness where practical.

### Security

Management operations must be authorized independently from read-only status access where applicable.

## Architecture Impact

Defines YasinHub as a management/control-plane component rather than a universal application runtime.

## Evidence

- `YASIN_AI_CONTEXT.md`
- `docs/architecture/`
- YasinHub project architecture/status-store documentation

Exact APIs and runtime contracts remain subject to source verification.

## Related Documents

- ADR-0001
- ADR-0002
- ADR-0003

## Open Questions

- Which management operations are authoritative versus advisory?
- What is the formal status schema and freshness contract?
