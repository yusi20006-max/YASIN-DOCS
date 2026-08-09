# Phase 8 — Code Audit Next Pass

- Date: 2026-08-09
- Status: Planned execution pass
- Purpose: move from README-level architectural verification to source/configuration/test verification before ADR acceptance

## Audit Principle

The ecosystem architecture must be derived from implementation evidence rather than inferred from project names or README summaries.

```text
Source / Tests / Config
        ↓
Implementation Reality
        ↓
Architecture Model
        ↓
ADR Acceptance
```

## Audit Matrix

| Area | Repository | Inspect | Required Output |
|---|---|---|---|
| Core public API | Yasin-core | package exports, SDK, runtime, agents, execution | verified API/boundary map |
| Core providers | Yasin-core | provider interfaces/adapters/config | provider ownership map |
| Core storage | Yasin-core | storage modules/config/tests | storage ownership map |
| Agent integration | Yasin-agent | Core imports/client, planner, executor, tools, sessions | Core↔Agent dependency map |
| Hub implementation | YasinHub | CLI, status store, process checker, registry, service behavior | current Hub boundary |
| Relay pipeline | YasinRelay | collector, normalizer, validator, dedup, AI, media, publisher, scheduler, storage | actual Relay pipeline graph |
| Feed pipeline | Yasinfeed | fetch, process/rewrite, scheduler, storage, publishers | actual Feed pipeline graph |
| CLI integration | Yasin-cli | commands, service definitions, adapters, subprocess/API integration | actual control-surface map |
| AI platform | Yasin-AI | provider, plugin, persistence, API/runtime boundaries | AI capability/trust map |
| Cross-project contracts | all above | dependency files, URLs, SDK usage, schemas, tests | contract matrix |

## Required Classification

Every discovered relationship must be classified as one of:

- `RUNTIME_DEPENDENCY`
- `API_DEPENDENCY`
- `CLI/SUBPROCESS_INTEGRATION`
- `DATA/SCHEMA_DEPENDENCY`
- `OPTIONAL_INTEGRATION`
- `DOCUMENTATION_ONLY`
- `UNKNOWN`

## ADR Impact Rules

- Evidence confirming the current wording → keep `Proposed`, candidate for `Accepted` after maintainer review.
- Evidence narrowing the wording → revise ADR before acceptance.
- Evidence contradicting the wording → mark `Needs Rewrite` and update architecture documents.
- Insufficient evidence → keep `Proposed`; do not infer.

## Mandatory Deliverables

1. `PHASE8_CODE_AUDIT_REPORT.md`
2. `docs/architecture/ECOSYSTEM_CURRENT_STATE.md` update
3. `docs/architecture/ECOSYSTEM_DEPENDENCY_MATRIX.md` update
4. ADR revisions for all `PARTIAL` or `CONFLICT` findings
5. Acceptance recommendation matrix with source evidence

## Critical Current Issue

ADR-0010 must remain unaccepted until the overlap between YasinFeed and YasinRelay publishing/content-processing responsibilities is resolved or explicitly modeled as intentional.

## Completion Criterion

Phase 8 source verification is complete only when every first-class ecosystem repository has at least one source-level evidence record and every ecosystem-wide ADR has a `CONFIRMED`, `PARTIAL`, `CONFLICT`, or `UNVERIFIED` status backed by concrete implementation evidence.
