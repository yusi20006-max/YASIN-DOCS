# ADR-0002: Yasin-Core Runtime Boundary

- Status: Proposed
- Date: 2026-08-09
- Decision owners: Yasin ecosystem maintainers
- Scope: Yasin-Core and its consumers
- Supersedes: None
- Superseded by: None

## Context

Multiple Yasin projects require reusable runtime abstractions. Duplicating those abstractions inside agents, management tools, or applications would create divergent behavior and make cross-project compatibility difficult.

## Decision

Yasin-Core is the foundational boundary for reusable Yasin runtime abstractions. Consumer projects should depend on its stable public interfaces where those interfaces are explicitly verified as public.

Yasin-Core should not absorb application-specific responsibilities merely because they can technically be implemented there.

## Rationale

A dedicated foundation layer provides a stable location for shared runtime semantics while preserving higher-level ownership boundaries.

## Alternatives Considered

### Duplicate runtime logic in each consumer
Rejected because it increases divergence and maintenance cost.

### Put all ecosystem behavior into Yasin-Core
Rejected because it would turn the foundation into a monolithic application layer.

## Consequences

### Positive

- Shared runtime behavior has a clear owner.
- Consumers can remain focused on their domain responsibilities.
- API compatibility can be reviewed centrally.

### Negative / Trade-offs

- Core API changes can affect multiple consumers.
- Core must maintain strong compatibility discipline.

### Compatibility / Migration

Public Core contracts should evolve compatibly where practical. Breaking changes require impact analysis of known consumers.

## Architecture Impact

This establishes a boundary between foundation/runtime concerns and higher-level agent, AI, management, relay, feed, and CLI concerns.

## Evidence

- `YASIN_AI_CONTEXT.md`
- `docs/ai/AI_PROJECT_SELECTION_MATRIX.md`
- `docs/architecture/` project and system records
- Existing Yasin-Agent integration documentation referencing `yasin_core.sdk` / `YasinCoreClient`

The exact public symbol surface remains subject to source verification.

## Related Documents

- ADR-0001
- `docs/ai/AI_CHANGE_IMPACT_PROTOCOL.md`

## Open Questions

- Which Core symbols are formally stable public API?
- What compatibility/versioning policy should govern Core releases?
