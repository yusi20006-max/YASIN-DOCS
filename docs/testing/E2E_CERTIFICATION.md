# Cross-Repository E2E Certification Harness

**Issue:** YASIN-DOCS #15 (FINAL-02)  
**Depends on:** #11 mock integration harness, public Yasin-AI contracts v1.1.4

## Purpose

Deterministic offline verification of Yasin-AI → Relay / Feed / Press integration semantics without live or paid providers.

## Run

```bash
python -m tools.e2e_certification
pytest tools/e2e_certification/tests/ -q
```

## Coverage

| Repository | Checks |
|------------|--------|
| Yasin-AI-contracts | request/response fields, version compatibility |
| YasinRelay | success, fallback/passthrough on error |
| Yasinfeed | success, raise on error |
| YasinPress-Rewrite- | success, structured error (no raise) |
| ecosystem | offline, no secrets required |

Agent AI path is **skipped** while Yasin-agent #19 remains deferred.

## Failure output

Each result includes `repository` + `check` so CI identifies the violating contract owner.
