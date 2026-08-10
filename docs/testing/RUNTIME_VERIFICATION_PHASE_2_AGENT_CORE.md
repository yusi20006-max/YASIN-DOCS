# Runtime Verification — Phase 2: Yasin-Agent ↔ Yasin-Core

## Scope

Verify the Agent/Core integration boundary using repository source and declared integration tests.

## Evidence

Yasin-Agent v1.0.0 documents `YasinCoreClient`, `YasinCoreAgentAdapter`, SDK registration, task creation/execution, tool discovery, plugin discovery and isolated memory/context as Core integration surfaces.

The repository contains `tests/test_integration.py` with executable integration coverage for Core client initialization, agent registration/task execution, memory/context handling, agent definition propagation, SDK tool discovery/registration/execution, and SDK plugin discovery/registration/execution.

## Verification Matrix

| Check | Evidence | Status |
|---|---|---|
| Core SDK import | `from yasin_core.sdk import ...` | VERIFIED |
| Core client construction | `test_core_client_initialization` | VERIFIED |
| Agent registration into Core | `register_all_agents` + `list_agents` assertion | VERIFIED |
| Core task creation | `client.create_task(...)` | VERIFIED |
| Core task execution | `client.execute_task(...)` | VERIFIED |
| Execution result contract | status/result/error assertions | VERIFIED |
| Context propagation | `get_current_context()` assertions | VERIFIED |
| Core-backed memory | memory helper calls + round-trip assertions | VERIFIED |
| Tool integration | SDK register/discover/execute path | VERIFIED |
| Plugin integration | register/discover/execute path | VERIFIED |
| Actual test-run result | CI/local execution evidence | OPEN |

## Important Qualification

`VERIFIED` means the integration contract is present in source and represented by executable tests. It does **not** mean those tests were executed during this audit turn. No unobserved pytest/CI result is promoted to PASS.

## Architecture Assessment

```text
Yasin-Agent
    ↓
YasinCoreClient
    ↓
Agent registration
    ↓
Core task creation/execution
    ↓
Context / Memory / Tools / Plugins
```

The integration test suite explicitly exercises this path.

## Remaining Runtime Evidence

To convert this phase to an execution-backed PASS, run in an environment containing the compatible Yasin-Core package:

```bash
pip install -e .
pytest tests/test_integration.py -v
```

Prefer testing against the real Yasin-Core package rather than relying only on the fallback/mock loader described by the repository.

## Exit Criteria

```text
Integration source evidence       VERIFIED
Integration test coverage         VERIFIED
Real Core execution               OPEN
Green test-run evidence            OPEN
No regression                      OPEN
```

## Status

**Phase 2 — integration contract verified; runtime execution evidence remains OPEN.**
