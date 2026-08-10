# Yasin-Agent — Project Knowledge Pack

## Identity
- Repository: `yusi20006-max/Yasin-Agent`
- Package identity in README: `agent_platform`
- Role: agent definition, planning, workflow execution, tools, plugins, sessions, memory/context integration.
- README states stable version `1.0.0`.

## Owns
- Agent definitions and metadata
- Planner / workflow templates
- Task state machine
- Sequential executor with validation/retry
- Tool registration and invocation
- Plugin discovery/integration
- Session and context isolation
- Core SDK integration adapter

## Does Not Own
- Generic low-level runtime foundations that belong in Core
- Ecosystem lifecycle control owned by Hub
- Unified ecosystem UX owned by CLI
- Product-specific content publishing logic

## Core Relationship
```text
Yasin-Agent
     ↓
Yasin-Core SDK
```

The README explicitly provides `YasinCoreAgentAdapter` and demonstrates registration/execution through `YasinCoreClient`.

## Main Components
`agent_definition.py`, `agent_registry.py`, `task.py`, `state_machine.py`, `planner.py`, `executor.py`, `tool_runner.py`, `memory_context.py`, `integration.py`, `cli.py`.

## Execution Model
```text
Agent Definition
      ↓
Planner
      ↓
Task / StateMachine
      ↓
Executor
      ↓
Tools / Plugins
      ↓
Validated Result
```

Retries and validation are part of execution semantics.

## CLI Boundary
The package has a local CLI integration layer, but it should not become the ecosystem-wide command/control plane. YasinCLI remains the unified ecosystem UX.

## Testing
README documents `pytest tests/ -v` and includes tests for agent/platform behavior, memory/context, and integration.

## Change Rules
Changes to Core SDK integration, task lifecycle contracts, tool interfaces, or public agent interfaces should trigger compatibility review. Do not couple Agent to Hub internals.

## AI Agent Brief
For agent/workflow behavior, inspect Yasin-Agent first. For generic runtime/SDK primitives, inspect Core. For lifecycle/status operations, inspect Hub/CLI rather than adding operational logic to Agent.
