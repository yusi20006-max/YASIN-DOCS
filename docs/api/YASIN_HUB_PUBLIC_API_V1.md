# YasinHub — Public API & Control Surface v1

## Evidence

Source-verified from `yusi20006-max/YasinHub` README and public package modules.

Repository package version: `1.0.0`.

## Role

YasinHub is a lightweight ecosystem status, control, and integration layer. Its current implementation is centered on project status records, process inspection, project registry, reporting, CLI control, and integrations with Yasin-Core, Yasin-Agent, and Yasin-Relay.

The repository explicitly describes the CLI as the central control layer for the Yasin ecosystem. fileciteturn177file0

## 1. Public Package Exports

`yasinhub.__all__` exports:

```text
ProcessStatus
check_process
ProjectEntry
default_registry
ProjectReport
build_report
StatusRecord
read_all_statuses
read_status
write_status
CoreIntegration
```

Package version:

```text
1.0.0
```

These exports are source-verified from `yasinhub/__init__.py`. fileciteturn178file0

## 2. Status Store Contract

### Contract ID

`HUB-STATUS-STORE`

### Public symbols

```text
StatusRecord
write_status
read_status
read_all_statuses
```

### Storage boundary

Default status directory:

```text
~/.yasin_status/
```

Each project writes a JSON status record named:

```text
<project>.json
```

The documented basic payload is:

```json
{
  "last_run": "ISO-8601 timestamp",
  "success": true,
  "message": "..."
}
```

`StatusRecord` also models optional `health`, `metrics`, and `db_stats` dictionaries. fileciteturn179file0

### `write_status`

Source-verified signature:

```python
write_status(
    project: str,
    success: bool,
    message: str = "",
    status_dir: Optional[Path] = None,
) -> Path
```

Behavior:

- creates the status directory when necessary;
- writes JSON using UTF-8;
- records current UTC time;
- returns the resulting `Path`.

### `read_status`

Source-verified signature:

```python
read_status(
    project: str,
    status_dir: Optional[Path] = None,
) -> Optional[StatusRecord]
```

Invalid JSON is represented as a `StatusRecord` containing an invalid/corrupt-file message rather than raising `JSONDecodeError`.

### `read_all_statuses`

Source-verified signature:

```python
read_all_statuses(
    status_dir: Optional[Path] = None,
) -> Dict[str, StatusRecord]
```

It scans `*.json` status files and returns records keyed by project name.

## 3. Project Registry Contract

### Public symbols

```text
ProjectEntry
default_registry
```

`ProjectEntry` fields are source-verified:

```python
ProjectEntry(
    name: str,
    path: Optional[str] = None,
    process_pattern: Optional[str] = None,
    description: str = "",
    start_command: Optional[str] = None,
    stop_command: Optional[str] = None,
)
```

The registry supports YAML-backed configuration with fallback defaults. fileciteturn180file0

The current default registry contains application/service entries including YasinFeed, YasinRelay, Yasin-Agent, Yasin-AI, YasinPress and supporting projects. This list is an operational registry, **not proof of runtime dependency**.

## 4. Core Integration Contract

### Contract ID

`HUB-CORE-SDK`

### Public symbol

```text
CoreIntegration
```

YasinHub imports:

```python
from yasin_core.sdk import YasinCoreClient
from yasin_core.compatibility import is_compatible
```

The integration therefore confirms a concrete:

```text
YasinHub → Yasin-Core SDK
```

boundary. fileciteturn182file0

### Compatibility policy

Hub defines:

```text
CORE_VERSION_COMPAT = ">=1.0.0"
```

and delegates compatibility checking to Core's `is_compatible` when available.

### Public methods

Source-verified methods include:

```text
CoreIntegration.__init__(client=None)
CoreIntegration.check_health()
CoreIntegration.get_runtime_info()
```

### `check_health()` result

The method returns a dictionary containing:

```text
status
connected
error
version
compatibility
```

When connected, it obtains the Core version through:

```text
client.get_version()
```

### `get_runtime_info()`

The integration consumes these Core SDK calls:

```text
list_agents()
list_tools()
list_plugins()
list_providers()
get_info()
```

and returns them under:

```text
agents
tools
plugins
providers
client_info
```

## 5. CLI Control Surface

The CLI module documents and implements these command families:

```text
status
core
dashboard
agent
relay
start
stop
restart
doctor
```

Agent subcommands:

```text
agent register <name> [--description]
agent status <name>
agent health <name>
agent start <name>
agent stop <name>
agent restart <name>
```

Relay subcommands include:

```text
relay connect
relay status
relay event <event_type> <payload>
relay verify-channels [channels]
```

Service lifecycle commands:

```text
start [service|all]
stop [service|all]
restart [service|all]
```

The CLI also exposes:

```text
core
 doctor
 dashboard [--live] [--interval SECONDS]
```

The source explicitly identifies this CLI as the central ecosystem control layer. fileciteturn181file0

## 6. Architectural Boundary

Current implementation-backed boundary:

```text
                    YasinHub
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   Status Store     Core SDK      Project adapters
        │              │              │
        ▼              ▼              ├── Agent
    JSON files      Yasin-Core         └── Relay

                       ▲
                       │
                    CLI user
```

YasinHub should consume public project interfaces rather than private implementation modules.

## 7. Important Architectural Correction

The current source demonstrates a **real Hub → Core SDK dependency**.

It also demonstrates operational knowledge of multiple projects through the registry, but registry membership must not automatically be interpreted as import-level dependency.

Therefore:

```text
Hub registry entry ≠ dependency
Hub adapter/import   = dependency/integration evidence
```

## 8. Contract Status Update

`HUB-CONTROL` is now:

**Source-verified for the current CLI/control surface.**

`HUB-CORE-SDK` is:

**Source-verified.**

`HUB-STATUS-STORE` is:

**Source-verified.**

Exact AgentIntegration and RelayIntegration method signatures require their respective source files for a complete adapter contract.

## 9. AI Agent Rules

When changing YasinHub:

1. Preserve the public exports in `yasinhub.__init__` unless intentionally changing the public API.
2. Treat status JSON as an explicit integration contract.
3. Do not assume registry membership creates a dependency.
4. Keep Core interaction behind the Core SDK boundary.
5. Preserve Core compatibility validation.
6. Do not move project-specific business logic into Hub merely to simplify CLI commands.
7. Update this document when exported APIs or command contracts change.
8. Update the ecosystem Contract Registry for cross-project contract changes.
9. Add an ADR when a new architectural dependency is introduced.

## 10. Open Work

For full contract completeness, audit:

```text
agent_integration.py
relay_integration.py
process_checker.py
report.py
config_manager.py
dashboard.py
```

and extract exact signatures, return schemas, exceptions, command exit codes, and adapter behavior.

## Status

**YasinHub Public API & Control Surface v1 — source-verified baseline complete.**
