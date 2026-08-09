# Phase 8 — YasinHub Code Audit Pass 1

- Date: 2026-08-09
- Repository: `yusi20006-max/YasinHub`
- Status: Evidence recorded

## 1. Actual Role

YasinHub is currently a lightweight local ecosystem status/operations observer, not the implementation runtime of the Yasin projects it monitors.

Its stated purpose is to answer what is running, when it last ran, and whether the last execution succeeded.

## 2. Status Contract

Projects write a JSON status record through `write_status(project, success, message)` into a shared status directory, normally `~/.yasin_status/`.

The status record supports `last_run`, `success`, `message`, `health`, `metrics`, and `db_stats`. This creates a simple cross-project observability contract that other Yasin services can publish into.

## 3. Project Registry

`registry.py` defines `ProjectEntry` with name, path, process pattern, description, start command, and stop command. The current default registry contains YasinFeed, YasinRelay, Yasin-Agent, Yasin-AI, YasinCoder, YasinPress, Backup Manager, and an Eitaa news process.

This is important ecosystem evidence: Hub already treats several Yasin projects as independently managed components.

## 4. Process/Health Model

`report.py` combines two signals:

```text
Project process state
        +
Last reported execution state
        ↓
Unified ProjectReport
```

Health states include `RUNNING`, `FAILED`, `SUCCESS`, `STALE`, `UNKNOWN`, and `IDLE`. PID files are checked first when available; otherwise the configured process pattern is used.

## 5. Architectural Boundary

```text
                   Yasin Ecosystem
                         │
       ┌─────────────────┼──────────────────┐
       ↓                 ↓                  ↓
   Yasin-Core       Yasin-Agent         Yasin-AI
       │                 │                  │
       └─────────────────┼──────────────────┘
                         ↓
                    YasinHub
                         │
              ┌──────────┴──────────┐
              ↓                     ↓
        Status Contract       Process/Health
              │                     │
              └──────────┬──────────┘
                         ↓
                  Operator View
```

Hub should therefore be modeled as a **control/observability plane**, not as a dependency of Core, Agent, or AI business logic.

## 6. Important Distinction

YasinHub contains `start_command` and `stop_command` metadata, but the inspected architecture establishes status/reporting as its core role. The existence of command metadata is not yet proof that Hub is the authoritative lifecycle manager for every project. That requires inspection of command-execution code.

## 7. ADR Impact

| Area | Result |
|---|---|
| Hub as ecosystem observer | **CONFIRMED** |
| Cross-project status contract | **CONFIRMED** |
| Process health aggregation | **CONFIRMED** |
| Hub → Core runtime dependency | **NOT CONFIRMED** |
| Hub as authoritative process manager | **UNRESOLVED** |
| Hub as ecosystem control plane | **PARTIAL / likely** |

## 8. Current Dependency Model

```text
Yasin-Core ───────┐
Yasin-Agent ──────┤
Yasin-AI ─────────┤
YasinRelay ───────┤──→ status contract → YasinHub
YasinFeed ────────┤
YasinPress ───────┤
YasinCoder ───────┤
                  │
                  ↓
             Operator report
```

The arrow represents reporting/observation, not necessarily a runtime import dependency.

## 9. Next Pass

Inspect `cli.py`, `config_manager.py`, `process_checker.py`, `pid_store.py`, and tests to determine whether Hub is only an observer or also an active lifecycle/control manager. Then reconcile Hub's registry with the canonical repository list in YASIN-DOCS.
