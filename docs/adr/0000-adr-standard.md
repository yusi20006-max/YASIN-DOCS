# ADR-0000: Yasin Architecture Decision Record Standard

- **Status:** Accepted
- **Date:** 2026-08-11
- **Scope:** Yasin ecosystem

## Context

Yasin is composed of multiple repositories with different responsibilities. Architectural decisions that cross repository boundaries must remain explicit, reviewable, and separated from implementation details.

## Decision

Yasin-DOCS uses Architecture Decision Records (ADRs) as the canonical record for intentional architectural decisions.

Each ADR should contain:

1. Title and identifier
2. Status: Proposed, Accepted, Superseded, Deprecated, or Rejected
3. Date
4. Context / problem
5. Decision
6. Consequences
7. Alternatives considered when relevant
8. Evidence and affected repositories when the decision depends on existing implementation

ADRs are numbered sequentially and stored under `docs/adr/`.

An ADR is required when a change intentionally modifies one or more of the following:

- cross-project responsibility or ownership;
- public API or integration contracts;
- data ownership or storage boundaries;
- agent/runtime boundaries;
- AI provider architecture;
- publishing/feed/relay topology;
- CLI/control-plane responsibilities;
- security or trust boundaries;
- compatibility policy;
- documentation governance.

A bug fix or local refactor does not require an ADR unless it changes an architectural boundary.

## Consequences

- Architectural intent is preserved independently from source-code history.
- AI coding agents can identify decisions before making cross-project changes.
- Superseded decisions remain traceable rather than silently disappearing.
- Implementation repositories remain the source of truth for code behavior; ADRs record why the architecture is intentionally shaped that way.

## Evidence rule

An ADR must distinguish existing facts from proposed design. Repository/source evidence should be cited in the ADR when the decision depends on current implementation.
