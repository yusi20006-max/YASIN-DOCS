# ADR-0011: Centralized Yasin Documentation Governance

- Status: Proposed
- Date: 2026-08-09
- Decision owners: Yasin ecosystem maintainers
- Scope: YASIN-DOCS and ecosystem documentation
- Supersedes: None
- Superseded by: None

## Context

The Yasin ecosystem spans multiple repositories and requires architecture, decisions, evidence, AI onboarding, operational guidance, and project-specific documentation. Without a central governance layer, architectural intent can become fragmented and AI agents may receive inconsistent or incomplete context.

## Decision

`YASIN-DOCS` is the centralized documentation and architecture-knowledge layer for the Yasin ecosystem.

It coordinates ecosystem architecture, project registry and boundaries, architecture graphs, ADRs, AI context and onboarding, evidence policy, cross-project impact guidance, and documentation navigation.

`YASIN-DOCS` documents and governs architectural knowledge; it does not become the runtime owner of the systems it documents.

Project repositories remain responsible for implementation-local documentation, source code, tests, configuration, and operational details specific to that project.

## Rationale

A centralized architecture layer provides a stable entry point for humans and AI agents while preserving repository ownership and implementation autonomy.

## Alternatives Considered

### Documentation only inside each repository
Rejected as the sole model because ecosystem-wide relationships and decisions would be fragmented.

### Put all project documentation into YASIN-DOCS
Rejected because local implementation documentation belongs with the implementation repository.

### Make YASIN-DOCS a runtime dependency
Rejected because documentation ownership and runtime execution are separate concerns.

## Consequences

### Positive

- One ecosystem-wide architecture entry point.
- Consistent AI onboarding.
- Central ADR and decision history.
- Easier cross-project impact analysis.
- Clear separation between intent and implementation.

### Negative / Trade-offs

- Documentation must be actively synchronized.
- Central documents can become stale if repositories evolve without documentation updates.
- Governance adds review overhead for architectural changes.

### Operational

Documentation should identify evidence and freshness where practical. Changes to significant architecture should trigger documentation review.

### Security

No secrets, private credentials, tokens, or sensitive operational material should be stored in public architecture documentation.

### Compatibility / Migration

New ecosystem projects should be registered in YASIN-DOCS and assigned a documented architectural scope before being treated as established ecosystem components.

## Architecture Impact

Establishes the documentation boundary around the complete ecosystem while keeping implementation ownership in individual repositories.

## Evidence

- `YASIN_AI_CONTEXT.md`
- `docs/ai/AI_INDEX.md`
- `docs/architecture/`
- `docs/adr/ADR_STANDARD.md`
- `ROADMAP.md`

## Related Documents

- ADR-0001
- ADR-0009
- `docs/ai/AI_ONBOARDING.md`
- `docs/ai/AI_EVIDENCE_POLICY.md`

## Open Questions

- What automated synchronization checks should run when ecosystem repositories change?
- Which documentation classes require mandatory review before merge?
- What freshness/SLA should apply to verified architecture records?
