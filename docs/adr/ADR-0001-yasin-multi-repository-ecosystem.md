# ADR-0001: Yasin Multi-Repository Ecosystem

- Status: Proposed
- Date: 2026-08-09
- Decision owners: Yasin ecosystem maintainers
- Scope: Ecosystem-wide
- Supersedes: None
- Superseded by: None

## Context

Yasin is developed as multiple repositories with different responsibilities. Treating the entire system as one undifferentiated codebase would blur ownership, make changes harder to validate, and increase the risk of duplicating responsibilities across projects.

The ecosystem therefore needs explicit repository boundaries and a central architectural knowledge layer.

## Decision

Yasin is maintained as a coordinated **multi-repository ecosystem** in which each project has an explicit primary responsibility and integration boundary.

`YASIN-DOCS` serves as the central architecture and decision documentation layer, but it does not become a runtime dependency merely because it documents the ecosystem.

## Rationale

Explicit repository boundaries allow focused ownership, independent testing and release workflows, clearer public contracts, smaller changes, easier AI-assisted development, and controlled cross-project impact analysis.

## Alternatives Considered

### Monolithic repository
Rejected as the default architectural model because it would collapse independent responsibility boundaries and increase coupling.

### Independent projects with no central architecture layer
Rejected because cross-project intent, contracts, and decisions would become fragmented.

## Consequences

### Positive

- Clearer ownership.
- Easier repository-level work.
- Cross-project changes become explicit.
- AI agents can select an owner before editing.

### Negative / Trade-offs

- Cross-project changes require coordination.
- Documentation must remain synchronized with implementation.
- Contract changes can require multiple repository updates.

### Operational

Repository status, source, tests, and configuration remain authoritative for implementation details. YASIN-DOCS records architecture and intent.

### Security

Separate repositories do not automatically imply separate trust boundaries. Security boundaries must be explicitly documented and verified.

### Compatibility / Migration

New projects should define their responsibility and integration contracts before being treated as first-class ecosystem components.

## Architecture Impact

The decision establishes the top-level ecosystem boundary and supports the project registry, architecture graphs, AI project-selection matrix, and cross-project impact protocol.

## Evidence

- `YASIN_AI_CONTEXT.md`
- `docs/architecture/`
- `docs/ai/AI_PROJECT_SELECTION_MATRIX.md`
- `docs/ai/AI_CHANGE_IMPACT_PROTOCOL.md`
- `ROADMAP.md`

The detailed repository implementation remains subject to source verification.

## Related Documents

- `ADR_STANDARD.md`
- `README.md`
- `YASIN_AI_CONTEXT.md`

## Open Questions

- Which repositories should be formally classified as core, supporting, experimental, or external integrations?
- Which cross-project contracts should receive independent versioning?
- What release coordination policy should govern synchronized changes?
