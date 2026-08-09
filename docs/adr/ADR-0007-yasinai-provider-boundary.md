# ADR-0007: Yasin-AI Provider and AI Capability Boundary

- Status: Proposed
- Date: 2026-08-09
- Decision owners: Yasin ecosystem maintainers
- Scope: Yasin-AI and AI/provider consumers
- Supersedes: None
- Superseded by: None

## Context

Multiple Yasin components may require model inference, provider selection, retrieval, knowledge capabilities, or AI-assisted processing. Duplicating provider-specific integration throughout the ecosystem would create coupling and inconsistent behavior.

## Decision

Yasin-AI is the primary architectural boundary for reusable AI/provider capabilities. Provider-specific concerns should remain behind explicit interfaces so consumers depend on Yasin-level capabilities rather than embedding provider implementation details wherever possible.

Yasin-AI may expose provider selection and persistence mechanisms within its own scope, but it must not become the owner of unrelated application workflows.

## Rationale

This creates one place to manage provider abstractions, fallback behavior, AI-specific configuration, and AI capability contracts while allowing consumers to remain domain-focused.

## Alternatives Considered

### Each project integrates providers independently
Rejected as the default because it duplicates configuration, error handling, provider selection, and compatibility logic.

### Put all application workflows inside Yasin-AI
Rejected because AI capability ownership is different from application/domain ownership.

## Consequences

### Positive

- Centralized AI/provider boundary.
- Less provider-specific coupling in consumers.
- Easier provider replacement and fallback evolution.
- Consistent AI capability contracts.

### Negative / Trade-offs

- Yasin-AI becomes an important compatibility boundary.
- Provider failures can affect multiple consumers.
- Stable interfaces require deliberate versioning.

### Security

Provider credentials and sensitive configuration must remain outside source-controlled ADRs and must follow the ecosystem secret-management policy.

### Compatibility / Migration

Provider changes should be isolated behind the capability boundary where possible. Breaking capability changes require consumer impact analysis.

## Architecture Impact

Defines the AI/provider boundary and distinguishes AI capability from Agent orchestration, Core runtime, management, relay, and publishing responsibilities.

## Evidence

- `YASIN_AI_CONTEXT.md`
- `docs/architecture/`
- Yasin-AI project architecture documentation
- Existing documented local persistence/plugin boundaries

Exact provider interfaces and public symbols remain subject to source verification.

## Related Documents

- ADR-0001
- ADR-0002
- ADR-0003

## Open Questions

- What is the canonical AI capability interface?
- Which provider abstractions are stable public contracts?
- Where should provider routing/fallback policy be owned?
