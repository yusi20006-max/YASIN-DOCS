# YasinHub — Project Knowledge Pack

## Identity
- Repository: `yusi20006-max/YasinHub`
- Role: lightweight ecosystem status, process-health, registry, and operational visibility layer.

## Owns
- Status persistence
- Live process checking
- Project registry
- Aggregated operational reports
- Status-oriented CLI

## Current Structure
`status_store.py`, `process_checker.py`, `registry.py`, `report.py`, `cli.py`.

## Operational Model
Projects report status into Hub; Hub combines persisted status with live process checks. Projects without permanent processes can register with `process_pattern=None` for on-demand execution.

```text
Project Runtime
      ↓
write_status()
      ↓
YasinHub status store
      +
process checker
      ↓
aggregated report
      ↓
Hub CLI
```

## Boundary
Hub is the ecosystem control/observability plane, not the owner of application business logic. A project should not import Hub internals merely to execute its core work.

## Ecosystem Relationship
```text
YasinCLI → YasinHub → project operational controls
```

This operational relationship is distinct from runtime/package dependency.

## Testing
README documents `python3 -m pytest tests/ -v`.

## Change Rules
Changes to registry semantics, lifecycle contracts, status schema, or operational control should update ecosystem architecture, API/contract documentation, and possibly an ADR.

## AI Agent Brief
For status, health, process lifecycle, registry, or ecosystem operational behavior, inspect Hub first. Do not place project-specific business logic here.
