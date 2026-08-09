# Yasin-Agent — Project Architecture Record

## Identity

- Repository: `yusi20006-max/Yasin-agent`
- Documented package: `agent_platform`
- Documented version: `1.0.0 stable`
- Role: transport-agnostic agent/workflow execution platform

## Responsibility

Yasin-Agent provides structured agent definitions, planning/workflows, task state management, sequential execution, retries, output validation, dynamic tools, plugins, memory/context/session handling, and a Yasin-Core SDK adapter.

## Module Map

```text
agent_definition.py   agent metadata/config/profile/prompt handling
agent_registry.py     agent registration
 task.py              Task/TaskResult/StepResult
state_machine.py      task lifecycle state machine
planner.py             Step/TemplatePlanner
executor.py            sequential execution, retries, validation
tool_runner.py         dynamic tool registration/invocation
memory_context.py      memory/context/session isolation
integration.py         Yasin-Core SDK adapter/fallback
cli.py                 agent CLI integration
```

## Important Boundary

The README explicitly describes the layer as **transport-agnostic** and independent from CLI or network transport, allowing a web layer such as FastAPI to be placed above it.

## Core Integration

The package includes `YasinCoreAgentAdapter` and documents use of `yasin_core.sdk.YasinCoreClient`. This is strong README-level evidence of an integration boundary with Yasin-Core, but exact source-level contracts still require audit.

## Memory / Context

The project documents isolated session contexts and short-/long-term memory access through a `MemoryManager` associated with Yasin-Core.

## Testing

The repository documents tests for agent platform behavior, memory/context, and integration.

## Boundary / Risk

Do not treat the package's CLI helper as ownership of the ecosystem-wide YasinCLI. The README describes CLI integration, not control-plane ownership.

## Audit Status

**Level 3:** responsibility and module structure are strongly documented; source-level API, dependency pinning, CI and exact Core integration require audit.
