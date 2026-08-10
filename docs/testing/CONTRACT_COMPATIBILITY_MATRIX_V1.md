# Yasin Ecosystem — Contract Compatibility Test Matrix v1

## Purpose

Define the minimum compatibility checks required before an ecosystem release is considered contract-safe.

This is a test plan and evidence register, not a claim that every test has already executed.

## Status Vocabulary

```text
PASS       Evidence/test is available and successful.
PARTIAL    Boundary is known but behavior is not fully verified.
OPEN       Test still needs implementation/execution.
N/A        Contract does not apply.
```

## 1. Core Compatibility Matrix

| Contract | Consumer | Check | Status |
|---|---|---|---|
| CORE-SDK | Yasin-Agent | import/export compatibility | PASS |
| CORE-SDK | YasinHub | import/export compatibility | PASS |
| CORE-COMPAT | Yasin-Agent | version compatibility | PARTIAL |
| CORE-COMPAT | YasinHub | version compatibility | PARTIAL |
| CORE-COMPAT | YasinRelay | validator contract | OPEN |
| CORE-COMPAT | YasinCLI | validator contract | OPEN |
| CORE-CLIENT | Agent/Hub | client construction/lifecycle | PARTIAL |
| CORE-PROVIDER | AI consumers | provider abstraction | PARTIAL |
| CORE-API | service consumers | request/response/error compatibility | OPEN |

## 2. Agent / Hub / Relay

| Contract | Check | Required Evidence | Status |
|---|---|---|---|
| AGENT-CORE | Agent starts against supported Core | integration test | OPEN |
| HUB-CORE | Hub starts against supported Core | integration test | OPEN |
| RELAY-PIPELINE | Pipeline stages preserve context | integration test | OPEN |
| RELAY-AI-PROCESSOR | provider adapter preserves processor contract | adapter test | OPEN |
| RELAY-PUBLISHER | publisher contract survives provider changes | publisher test | OPEN |

## 3. Feed / Press

| Contract | Check | Status |
|---|---|---|
| FEED-FETCH | normalized feed output | OPEN |
| FEED-REWRITE | rewrite input/output schema | OPEN |
| FEED-STORAGE | persistence round-trip | OPEN |
| PRESS-RSS-COLLECTOR | normalized news record | OPEN |
| PRESS-DEDUPE | duplicate detection invariants | OPEN |
| PRESS-AI | AI failure fallback | PARTIAL |
| PRESS-PUBLISH-QUEUE | restart/resume durability | OPEN |
| PRESS-EITAA-PUBLISHER | publish contract | OPEN |

## 4. Yasin-AI

| Contract | Check | Status |
|---|---|---|
| AI-SERVICE | request/response schema | OPEN |
| AI-MEMORY | persistence round-trip | OPEN |
| AI-PLUGIN | trusted in-process plugin lifecycle | OPEN |
| AI-PERSISTENCE | SQLite boundary | OPEN |
| AI-DEPLOYMENT | production configuration invariants | PARTIAL |

## 5. CLI

CLI remains planned, therefore these are acceptance tests rather than passing implementation tests.

| Contract | Acceptance Test | Status |
|---|---|---|
| CLI-STATUS | reports component state through public contracts | OPEN |
| CLI-DOCTOR | detects broken/mismatched components | OPEN |
| CLI-LIFECYCLE | start/stop/restart without private internals | OPEN |
| CLI-ADAPTERS | adapter isolation per project | OPEN |

## 6. Version Compatibility Rules

A release must satisfy:

```text
Major API break
    → ADR required
    → compatibility validator update
    → migration notes
    → integration tests
```

For backward-compatible changes:

```text
Minor/Patch
    → contract registry update
    → regression tests
```

## 7. Negative Tests

The compatibility suite must explicitly verify that:

1. unsupported Core versions are rejected;
2. private module imports are not required by consumers;
3. missing optional AI providers trigger documented fallback behavior;
4. unavailable local persistence fails with a controlled error;
5. unsupported plugin execution is rejected rather than silently treated as sandboxed;
6. CLI adapters cannot mutate another project's private storage directly;
7. an unconfirmed dependency cannot become a runtime dependency merely by appearing in registry metadata.

## 8. Release Gate

The ecosystem is **not Contract-Green** until:

```text
Core public API tests              PASS
Agent ↔ Core integration            PASS
Hub ↔ Core integration              PASS
Relay pipeline contract             PASS
Feed contracts                      PASS
Press contracts                     PASS
AI service contract                 PASS
CLI adapter/lifecycle tests         PASS
Negative compatibility tests        PASS
ADR index                           COMPLETE
```

## 9. Current Gate Assessment

```text
Core API                     🟢 baseline verified
Agent/Core                   🟡 integration test expansion required
Hub/Core                     🟡 integration test expansion required
Relay                        🟡 contract tests required
Feed                         🟠 tests required
Press                        🟠 tests required
Yasin-AI                     🟠 service tests required
YasinCLI                     🔴 implementation/acceptance tests required
```

## 10. Execution Order

```text
1. Core SDK regression tests
2. Agent/Core integration
3. Hub/Core integration
4. Relay contract tests
5. Feed/Press contract tests
6. Yasin-AI service tests
7. CLI implementation + adapter tests
8. Negative compatibility suite
9. Full ecosystem smoke test
10. Final architecture gate
```

## Status

**Contract Compatibility Test Matrix v1 — test specification complete; full execution remains open.**
