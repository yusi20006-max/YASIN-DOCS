# Cross-repository public-contract boundary CI

**Issue:** YASIN-DOCS #10

## Goal

Reliable CI that fails if any Yasin-AI *consumer* imports private implementation modules.

## Allowed imports

- `yasinai`
- `yasinai.contracts` (+ public submodules)
- `yasinai.services` (+ public submodules)
- `yasinai.providers` (+ public submodules)

## Forbidden imports

- `knowledge_platform`
- `security_platform`
- `developer_platform`
- Non-public `yasinai.*` packages (`yasinai.core`, `yasinai.cli`, `yasinai.private_modules`, …)

Comments, docstrings, and string literals do **not** count as imports (AST-based scan).

## Usage

```bash
# Fixture self-check (always run in CI)
python -m tools.contract_boundary tools/contract_boundary/tests/fixtures/good
python -m tools.contract_boundary tools/contract_boundary/tests/fixtures/bad   # expect exit 1

# Live consumer trees (optional)
python -m tools.contract_boundary /path/to/YasinRelay /path/to/Yasinfeed
```

## CI

Workflow: `.github/workflows/contract-boundary.yml`

- Always: unit tests + fixture scans
- Optional (`workflow_dispatch`): live checkout of consumers

## Acceptance

See issue #10 acceptance criteria.
