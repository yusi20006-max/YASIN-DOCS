# ADR-0008: Component-Scoped Storage Ownership

- Status: Proposed
- Date: 2026-08-09
- Decision owners: Yasin ecosystem maintainers
- Scope: Ecosystem data and persistence
- Supersedes: None
- Superseded by: None

## Context

Yasin components may need persistence for state, status, feeds, AI data, caches, or other domain information. A single implicit shared database would create hidden coupling, unclear ownership, and difficult migrations.

## Decision

Storage is component-scoped by default. Each project owns the data required for its responsibility unless a shared storage service is explicitly designed, documented, versioned, and verified.

A component must not assume that another project's storage schema is an API simply because the underlying database is technically accessible.

## Rationale

Explicit storage ownership makes data boundaries visible and reduces accidental coupling through direct database access.

## Alternatives Considered

### One shared database for the ecosystem
Rejected as the default because it creates strong coupling and makes schema ownership ambiguous.

### Unrestricted direct access to another component's database
Rejected because it bypasses the owning component's contract and makes migrations unsafe.

## Consequences

### Positive

- Clear data ownership.
- Independent schema evolution.
- Easier component isolation and testing.
- Reduced accidental cross-project coupling.

### Negative / Trade-offs

- Cross-project data access requires explicit APIs or contracts.
- Some data may need synchronization or duplication.
- Multiple stores can increase operational complexity.

### Security

Database access must follow the owning component's authorization and secret-management boundaries. Shared credentials are not implied by shared ecosystem membership.

### Compatibility / Migration

Schema changes are owned by the component responsible for the store. Consumers should depend on versioned contracts rather than undocumented tables.

## Architecture Impact

Defines storage ownership as a first-class architectural boundary and supports the ecosystem storage/configuration/security graph.

## Evidence

- `YASIN_AI_CONTEXT.md`
- `docs/architecture/`
- Existing documented YasinHub status storage
- Existing documented YasinRelay SQLite persistence
- Existing documented Yasin-AI local SQLite persistence

Exact schemas and cross-project access paths remain subject to source verification.

## Related Documents

- ADR-0001
- ADR-0004
- ADR-0005
- ADR-0007

## Open Questions

- Which data contracts require shared service semantics?
- Which stores need backup/retention guarantees at ecosystem level?
- Which schemas should receive explicit version identifiers?
