# YasinHub — Project Architecture Record

## Identity

- Repository: `yusi20006-max/YasinHub`
- Role: lightweight ecosystem status/health registry and CLI

## Responsibility

YasinHub records the status of projects/processes and reports current process state plus latest execution information.

## Module Map

```text
yasinhub/
├── status_store.py      read/write JSON status files
├── process_checker.py   live process checking via pgrep -f
├── registry.py          monitored-project registry
├── report.py            combine status + process state
└── cli.py               status command
```

## Usage Model

Projects such as YasinRelay can call `write_status(...)` after execution. Operators can run `python3 -m yasinhub.cli status` to view the combined report.

## Boundary

YasinHub is **not currently documented as a heavy dashboard or general runtime orchestrator**. It should not absorb application logic or agent workflows.

## Project Registry

The Hub has its own `DEFAULT_PROJECTS` registry. Projects without persistent processes can use a null process pattern, as documented for on-demand agent execution.

## Testing

The documented test command is `python3 -m pytest tests/ -v`.

## Audit Status

**Level 3:** responsibility and module structure are clear. Exact status-file schema, integration contracts, CLI exit behavior, and operational deployment need source-level audit.
