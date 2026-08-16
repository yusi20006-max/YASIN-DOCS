# Architecture boundary contract tests

**Issue:** YASIN-DOCS #12

## Goal

Automated policy checks for dependency direction and ownership rules of the Yasin ecosystem.

## Rules

| Code | Rule |
|------|------|
| AI-OWN-1 | Yasin-AI must not depend on domain apps (Relay/Feed/Press/Agent/Hub/CLI) |
| CONS-1 | Consumers must not depend on private Yasin-AI modules |
| CYCLE-1 | Circular dependency among canonical packages is detected |
| OWN-PIPE-1 | Domain pipeline orchestration stays in domain apps (not inside Yasin-AI) |

## Usage

```bash
python -m tools.architecture_boundary
pytest tools/architecture_boundary/tests/ -q
```

Policy is fixture / graph based — no multi-repo checkout required for unit tests.

## Alignment

Documents ADR-001 boundaries and `PIPELINE_OWNERSHIP.md`.
