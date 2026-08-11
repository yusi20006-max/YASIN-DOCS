# YasinFeed — CLI, Scheduler, Storage and Operational Audit v2

- Repository: `yusi20006-max/Yasinfeed`
- Branch audited: `main`
- Audit date: 2026-08-11
- Status: **Source-verified partial deep audit**

## CLI

`yasinfeed/cli/main.py` provides the following commands:

```text
status
start
stop
restart
doctor
config
version
```

The CLI is a real application control surface, not merely documentation. It can spawn the engine as a separate process, persist its PID, query the health API, stop the process using SIGTERM, and fall back to SIGKILL when graceful termination fails.

### Important boundary

The CLI owns user-facing lifecycle commands, while the engine owns module lifecycle. This is compatible with the ecosystem rule that **YasinCLI**, as the future unified ecosystem CLI, must orchestrate YasinFeed through a public boundary rather than importing and duplicating its internal implementation.

## `status`

The command first attempts the API health endpoint:

```text
/api/health
```

and falls back to:

```text
/health
```

It reports engine state, PID, uptime, module health checks, and metrics when available.

If the API is unavailable, it checks the stored PID and can distinguish a running process with an unresponsive API from a stopped engine.

## `start`

The CLI:

1. loads configuration;
2. checks whether an existing PID is alive;
3. launches `python -m yasinfeed.main` as a detached process group on non-Windows systems;
4. stores the child PID in `yasinfeed.pid`;
5. waits for initialization;
6. probes `/api/health`;
7. reports successful startup or delayed API readiness.

This is sufficient for standalone local operation.

## `stop`

The CLI reads `yasinfeed.pid`, verifies the process, sends SIGTERM, waits for termination, and escalates to SIGKILL if required. It removes the PID file afterward.

This provides an explicit lifecycle contract for external controllers.

## `restart`

`restart` is implemented as:

```text
stop → wait → start
```

This keeps lifecycle semantics centralized in the existing CLI instead of duplicating them elsewhere.

## `doctor`

The diagnostic command checks:

- Python version;
- required imports (`yaml`, `feedparser`, `sqlite3`);
- configuration availability;
- storage type/path;
- SQLite connection or JSON write access.

It computes an overall health state from these checks.

## `config`

Configuration output is recursively sanitized. Keys containing terms such as `key`, `secret`, `password`, or `token` are masked as `********` when populated.

This is an important operational safety boundary and should be preserved when integrating the future YasinCLI.

## `version`

The current implementation reports both CLI and engine versions. The package declares engine version `1.0.0`, while the CLI reports its own CLI version independently.

This distinction is useful for future ecosystem diagnostics because CLI and engine releases may evolve independently.

## Engine Lifecycle

`yasinfeed/engine.py` defines:

```text
initialize → start → running → stop
```

Initialization loads configuration, configures logging, dynamically imports the modules, instantiates them, and initializes them in registration order.

The registered order is:

```text
Monitoring
Integration
Storage
Models
Auth
Rewrite
Fetch
Publisher
Scheduler
API
```

Shutdown occurs in reverse order.

The engine also handles SIGINT/SIGTERM for graceful shutdown.

## Scheduler Role

The README assigns the scheduler to periodic task execution and background polling. It describes a default `fetch_and_process` pipeline that links:

```text
Fetch → Store → Rewrite → Publish
```

This is application-internal automation and must not be confused with YasinHub ecosystem orchestration.

## Storage Role

The documented production backend is SQLite, with an example path:

```text
data/yasinfeed.db
```

The `doctor` command performs an actual SQLite connection test and can create the parent directory when needed.

This confirms that storage is treated as an application-owned subsystem.

## Security / Configuration

The CLI's `config` command masks secrets before printing configuration. The production documentation also requires localhost API binding by default unless an explicit network security boundary exists.

## Current Findings

### Confirmed

- Standalone Python package.
- Independent CLI entry point.
- Lifecycle management.
- Background process/PID management.
- Health API probing.
- Installation diagnostics.
- Configuration inspection with secret masking.
- SQLite health check.
- Graceful process shutdown.
- Internal scheduler boundary.

### Remaining verification

The following source-level areas still require direct inspection before calling the YasinFeed audit complete:

1. scheduler implementation and retry semantics;
2. fetch/source manager implementation;
3. storage schema and migrations;
4. publisher implementations;
5. rewrite implementation;
6. API routes and authentication implementation;
7. actual tests and current CI results;
8. package dependency graph for hidden cross-project imports.

## Ecosystem Decision

YasinFeed remains independently runnable.

```text
YasinFeed ──X──> YasinPress
YasinFeed ──X──> YasinHub internals
YasinFeed ──X──> YasinCLI internals
```

External control is permitted through public commands/APIs. Internal runtime ownership remains inside YasinFeed.
