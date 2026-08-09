# AI Testing & Validation Protocol

## Goal

Never stop at “the code changed successfully.” Validate behavior and ecosystem impact.

## Validation Ladder

```text
Syntax/import check
      ↓
Focused unit tests
      ↓
Module tests
      ↓
Direct consumer tests
      ↓
Integration tests
      ↓
Cross-project validation
      ↓
Final diff/config/docs review
```

Do not run expensive levels when a cheaper failure already proves the change is incorrect.

## Change-to-Test Mapping

| Change | Minimum validation |
|---|---|
| documentation | Markdown/path/link review |
| internal function | focused unit tests |
| public API | unit + API/consumer tests |
| schema | migration + fixtures + consumer tests |
| config | loader/validation + affected runtime tests |
| message/event | producer + consumer + compatibility tests |
| runtime lifecycle | start/stop/health tests where available |
| deployment | build + deployment validation + health check |
| security boundary | security tests + negative cases |

## Failure Handling

When a test fails:

1. determine whether it is caused by the change;
2. inspect traceback/logs;
3. do not weaken the test merely to obtain green status;
4. distinguish environment failures from product failures;
5. report unresolved failures explicitly.

## Evidence Reporting

Every task report should state:

```text
Tests requested
Tests actually run
Passed
Failed
Skipped
Environment limitations
Remaining risk
```

## Cross-Project Validation

For L3/L4 changes, validate every known consumer or explicitly document why a consumer could not be tested.

## AI Rule

A passing local test suite does not prove ecosystem compatibility when a public cross-project contract changed.
