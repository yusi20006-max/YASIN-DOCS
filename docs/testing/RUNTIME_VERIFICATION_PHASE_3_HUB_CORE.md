# Runtime Verification — Phase 3: YasinHub ↔ Yasin-Core

## Scope

Verify whether YasinHub currently has a source-level/runtime integration boundary with Yasin-Core.

## Findings

YasinHub is currently a lightweight status/control CLI. Its documented responsibilities are status persistence, process checking, registry/report generation, and service management. The README does not declare a Yasin-Core SDK dependency.

Repository code-search for `yasin_core` and `core` returned no matching files/code references during this audit.

The Hub test suite covers its own status store, process checker, report builder, configuration loader, service manager, and CLI commands. It does not demonstrate a Core SDK integration test.

## Verification Matrix

| Check | Evidence | Status |
|---|---|---|
| YasinHub package exists | repository | VERIFIED |
| Hub status/control functionality | README + tests | VERIFIED |
| Yasin-Core import | no source evidence found | NOT CONFIRMED |
| Core client construction | no source evidence found | NOT CONFIRMED |
| Hub ↔ Core runtime call | no source evidence found | NOT CONFIRMED |
| Hub ↔ Core integration tests | no evidence found | NOT CONFIRMED |
| Hub CI workflow | no workflow evidence found | OPEN |
| Hub unit-test coverage | `tests/test_yasinhub.py` | VERIFIED |

## Architecture Assessment

The previous architecture assumption `YasinHub → Yasin-Core` must therefore remain **NOT CONFIRMED** as a runtime dependency.

YasinHub can currently be modeled as:

```text
YasinHub
├── status_store
├── process_checker
├── registry
├── report
├── service_manager
└── CLI
```

rather than asserting an unverified SDK coupling.

## Important Correction

This phase strengthens the dependency governance rule established by the Contract Registry:

```text
Architecture intent ≠ runtime dependency
Registry membership ≠ runtime dependency
```

If a future Hub implementation consumes Yasin-Core, it must introduce an explicit adapter/public API contract and executable integration tests.

## Exit Criteria

```text
Hub standalone behavior          VERIFIED
Core import                      NOT CONFIRMED
Hub/Core integration             NOT CONFIRMED
Integration test                 NOT CONFIRMED
CI evidence                      OPEN
```

## Status

**Phase 3 — Hub standalone contract verified; YasinHub ↔ Yasin-Core runtime dependency remains NOT CONFIRMED.**
