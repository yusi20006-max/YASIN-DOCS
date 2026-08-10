# Yasin-Agent — Public API Surface v1

## Evidence

**Source verified** from `yusi20006-max/Yasin-agent/agent_platform/__init__.py` and repository README.

Repository version identified by the package: `1.0.0`.

## Package

```text
agent_platform
```

The package explicitly exports the following public symbols through `__all__`.

## Public API

### Agent Registry

```text
AgentConfig
AgentNotFoundError
AgentRegistry
```

### Agent Definition

```text
AgentMetadata
AgentConfiguration
AgentProfile
PromptHandler
AgentDefinition
```

### Execution

```text
Executor
```

### Planning

```text
Planner
Step
TemplatePlanner
UnknownGoalError
```

### State Machine

```text
InvalidTransitionError
StateMachine
TaskState
```

### Tasks and Results

```text
StepResult
Task
TaskResult
```

### Tools

```text
ToolNotFoundError
ToolRunner
```

### Yasin-Core Integration

```text
YasinCoreAgentAdapter
get_active_client
register_all_agents
register_tool_via_sdk
discover_tools_via_sdk
register_plugin_via_sdk
discover_plugins_via_sdk
execute_plugin_via_sdk
```

### Agent Memory / Context

```text
MemoryManager
ContextManager
Session
SessionManager
save_agent_memory
get_agent_memory
```

## Public Surface Summary

```text
Agent Definition
      ↓
AgentRegistry
      ↓
Planner / TemplatePlanner
      ↓
Task / Step
      ↓
Executor
      ↓
ToolRunner
      ↓
Result / StateMachine

Integration boundary
      ↓
YasinCoreAgentAdapter
      ↓
Yasin-Core SDK
```

## Confirmed Integration

The repository README explicitly demonstrates:

```python
from yasin_core.sdk import YasinCoreClient
```

and uses `YasinCoreClient` with:

```text
AgentRegistry
TemplatePlanner
ToolRunner
register_all_agents
```

It also demonstrates `client.create_task(...)` and `client.execute_task(...)`.

Therefore the architectural contract:

```text
Yasin-Agent → Yasin-Core SDK
```

is source/documentation supported rather than merely inferred.

## CLI Boundary

The package exposes:

```text
agent_platform.cli.run_agent
agent_platform.cli.register_cli_command
```

The README documents the command concept:

```text
python -m agent_platform.cli agent run <agent_name>
```

The CLI is an integration surface; the core agent execution logic remains in the transport-independent package.

## Memory Boundary

The package exposes both:

```text
MemoryManager
ContextManager
Session
SessionManager
```

and helper functions:

```text
save_agent_memory
get_agent_memory
```

The README describes short-term/long-term session memory and isolated session context.

This should not be interpreted as a requirement that all ecosystem memory belongs to Yasin-Agent. The canonical architecture must continue to distinguish Agent session state from platform-level AI memory.

## Contract ID Update

This source audit upgrades:

```text
AGENT-SDK
```

from architecture-only evidence to **source-verified public surface evidence**.

Exact method signatures, constructor arguments, return schemas, exceptions raised by individual methods, and compatibility guarantees still require deeper source/test extraction.

## AI Agent Rules

When modifying Yasin-Agent:

1. Prefer the exported public API over private module internals.
2. Preserve `__all__` unless a deliberate public API change is intended.
3. Treat `YasinCoreAgentAdapter` as the explicit Core integration boundary.
4. Do not move transport concerns into the execution engine.
5. Preserve isolation between sessions and contexts.
6. Add/update tests when changing exported symbols.
7. Update the Contract Registry when public API behavior changes.
8. Record cross-project architectural changes in an ADR.

## Open Work

The next source-level extraction should inspect:

```text
agent_definition.py
agent_registry.py
planner.py
executor.py
state_machine.py
task.py
tool_runner.py
integration.py
memory_context.py
cli.py
```

to record exact signatures and lifecycle semantics.

## Status

**Yasin-Agent Public API v1 — source-level export inventory complete.**

Symbol-level signatures and behavioral contracts remain the next depth of audit.
