# Yasin Architecture Decision Record Standard

## 1. Purpose

Architecture Decision Records (ADRs) capture important architectural decisions, the reasoning behind them, their consequences, and their current status.

An ADR answers four questions:

1. What problem or decision required architectural attention?
2. What decision was made?
3. Why was it made instead of the alternatives?
4. What consequences and constraints does it create?

ADRs preserve architectural intent for humans and AI agents. They are not implementation tutorials and they are not substitutes for source-level documentation.

## 2. When an ADR Is Required

Create or update an ADR when a decision materially affects one or more of:

- system boundaries;
- repository ownership;
- public APIs or cross-project contracts;
- runtime architecture;
- agent architecture;
- AI/provider architecture;
- storage or data ownership;
- message/event contracts;
- security or trust boundaries;
- deployment topology;
- lifecycle/compatibility strategy;
- major technology selection;
- CLI/control-plane architecture;
- documentation governance.

An ADR is generally unnecessary for routine implementation details that do not alter architectural intent.

## 3. ADR Lifecycle

```text
Proposed
   ↓
Under Review
   ↓
Accepted ──────────────┐
   │                   │
   ↓                   ↓
Superseded           Deprecated
   │
   ↓
Historical
```

### Status meanings

- **Proposed** — decision is being prepared.
- **Under Review** — decision is being evaluated.
- **Accepted** — current architectural direction.
- **Deprecated** — no longer recommended, but not necessarily replaced.
- **Superseded** — replaced by a newer ADR.
- **Historical** — retained for architectural history only.

Do not delete an accepted ADR merely because it is no longer current. Preserve the decision history and link the replacement.

## 4. Numbering

Use monotonically increasing identifiers:

```text
ADR-0001
ADR-0002
ADR-0003
...
```

Do not reuse an identifier.

Recommended filename:

```text
ADR-0001-short-kebab-case-title.md
```

## 5. Required ADR Structure

Every ADR must use this structure unless a documented exception is justified.

```markdown
# ADR-NNNN: Title

- Status: Proposed | Under Review | Accepted | Deprecated | Superseded | Historical
- Date: YYYY-MM-DD
- Decision owners: ...
- Scope: ...
- Supersedes: ...
- Superseded by: ...

## Context

What problem, requirement, constraint, or architectural pressure led to this decision?

## Decision

What is the decision? State it directly and unambiguously.

## Rationale

Why was this decision selected?

## Alternatives Considered

### Alternative A

Description, benefits, drawbacks, and reason for rejection/selection.

### Alternative B

...

## Consequences

### Positive

...

### Negative / Trade-offs

...

### Operational

...

### Security

...

### Compatibility / Migration

...

## Architecture Impact

Which components, boundaries, contracts, flows, storage areas, or deployment assumptions change or are constrained?

## Evidence

Repository/file/source references supporting the decision.

## Related Documents

Links to architecture documents, issues, PRs, specifications, or other ADRs.

## Open Questions

Anything intentionally unresolved.
```

## 6. Evidence Rules

ADRs must distinguish facts from reasoning.

Use the ecosystem evidence vocabulary:

```text
Verified
Documented
Inferred
Candidate
Unknown
```

A decision may be based on constraints or judgment, but factual claims about current implementation should be traceable to evidence where practical.

Do not use an ADR to turn an assumption into a fact.

## 7. Decision Quality Requirements

A strong ADR should explain:

- the actual problem;
- the constraints;
- the selected option;
- important alternatives;
- why alternatives were rejected;
- trade-offs;
- compatibility consequences;
- security implications;
- operational implications;
- affected projects;
- migration or rollout requirements where applicable.

Avoid vague rationale such as “best practice” without explaining the concrete Yasin requirement it satisfies.

## 8. Cross-Project Decisions

For decisions affecting multiple repositories, explicitly identify:

```text
Producer
Consumer(s)
Contract
Compatibility requirements
Migration order
Ownership
Validation requirements
```

Cross-project ADRs should be referenced from the affected project architecture records when appropriate.

## 9. Superseding an ADR

Do not rewrite history to make an old decision look like the new decision.

Instead:

1. create a new ADR;
2. set the old ADR to `Superseded`;
3. link both directions;
4. explain what changed and why;
5. update the architecture documents that describe the current state.

## 10. Reversibility

Where relevant, state whether the decision is:

- easily reversible;
- reversible with migration;
- difficult to reverse;
- effectively irreversible.

Irreversible decisions require stronger rationale and review.

## 11. Security Decisions

Security-related ADRs must identify trust boundaries, threat assumptions, authorization implications, secret handling, and failure behavior when relevant.

Never place real credentials, tokens, private keys, or other secrets in an ADR.

## 12. AI Requirements

ADRs must be written so that a new AI agent can understand the decision without relying on hidden conversation history.

An AI agent must:

- read relevant ADRs before changing an architectural boundary;
- treat `Accepted` ADRs as current architectural intent unless superseded;
- inspect source when implementation reality matters;
- flag conflicts between code and ADRs instead of silently choosing one;
- update or create an ADR when a change materially alters architectural intent.

## 13. ADR Review Checklist

```text
[ ] Problem is clearly stated
[ ] Decision is explicit
[ ] Rationale is concrete
[ ] Alternatives considered
[ ] Trade-offs documented
[ ] Affected projects identified
[ ] Security impact considered
[ ] Compatibility/migration considered
[ ] Evidence included
[ ] Related documents linked
[ ] Status is correct
[ ] Supersession links are correct
[ ] No secrets included
[ ] AI can understand the decision without hidden context
```

## 14. Source of Truth

ADRs describe architectural intent and decisions. They do not override executable source, configuration, tests, or deployment reality by themselves.

When intent and implementation disagree:

1. identify the discrepancy;
2. determine whether implementation or architecture is stale;
3. fix the appropriate source;
4. update the ADR/documentation if the decision changed;
5. preserve historical context when useful.

## 15. Directory

All ecosystem ADRs belong under:

```text
docs/adr/
```

The ADR index should be maintained at:

```text
docs/adr/README.md
```

## 16. Golden Rule

**Record the decision and its reasoning, not just the final technology choice.**
