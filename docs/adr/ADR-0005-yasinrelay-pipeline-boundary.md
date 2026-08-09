# ADR-0005: YasinRelay Pipeline Boundary

- Status: Proposed
- Date: 2026-08-09
- Decision owners: Yasin ecosystem maintainers
- Scope: YasinRelay and relay/feed processing
- Supersedes: None
- Superseded by: None

## Context

Yasin requires a component responsible for relay, ingestion, and pipeline-oriented processing. Without a dedicated boundary, transport and pipeline behavior can leak into application components and become duplicated.

## Decision

YasinRelay owns relay and pipeline responsibilities within its defined scope. It should provide explicit integration boundaries rather than becoming a universal application layer for unrelated business logic.

## Rationale

A dedicated relay boundary isolates ingestion and pipeline concerns from management, agent, core runtime, and publishing responsibilities.

## Alternatives Considered

### Put relay logic into every consumer
Rejected because it duplicates transport and processing behavior.

### Make YasinRelay the owner of all content processing
Rejected because domain-specific processing and publishing remain owned by their respective components.

## Consequences

### Positive

- Clear pipeline ownership.
- Reusable relay behavior.
- Easier pipeline-specific testing and observability.

### Negative / Trade-offs

- Downstream consumers depend on relay contracts.
- Schema or transport changes can have cross-project impact.

### Compatibility / Migration

Relay contract changes require consumer analysis and appropriate migration planning.

## Architecture Impact

Establishes YasinRelay as a pipeline/relay boundary between ingestion-oriented flows and downstream components.

## Evidence

- `YASIN_AI_CONTEXT.md`
- `docs/architecture/`
- YasinRelay project architecture documentation

Exact transports, schemas, and public APIs remain subject to source verification.

## Related Documents

- ADR-0001
- ADR-0004

## Open Questions

- Which relay interfaces are stable public contracts?
- What event/message schemas require independent versioning?
