# FINAL-11 — Centralized Ecosystem Contract CI Activation

**Issue:** YASIN-DOCS #17  
**Date:** 2026-08-16

## Activation

Workflow: `.github/workflows/contract-boundary.yml`

### Jobs

1. **unit-and-fixtures** — scanner, architecture policy, integration harness, E2E certification (#15), secrets gate (#16)
2. **live-consumer-scan** — clones YasinRelay, Yasinfeed, YasinPress-Rewrite- and fails on private Yasin-AI imports
3. **architecture-policy-job** — forbidden graph edges / cycles

### Constraints

- No secrets, paid providers, or live LLM calls
- Public allowlist only: `yasinai.contracts`, `yasinai.services`, `yasinai.providers`
- Reproducible from clean checkout

### Local reproduction

```bash
pytest tools/ -q
python -m tools.e2e_certification
python -m tools.contract_boundary /path/to/consumer
python -m tools.architecture_boundary
python -m tools.security_gate tools docs .github
```
