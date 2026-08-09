# Phase 8 — Code Audit: Yasin-Agent Pass 2

- Date: 2026-08-09
- Status: Evidence recorded
- Repository: `yusi20006-max/Yasin-agent`

## Source Evidence

Direct inspection of `agent_platform/integration.py` confirms that the Core relationship is implemented in source code.

## Concrete Core SDK Imports

The integration layer imports `BaseAgent`, `YasinCoreClient`, `active_context`, `get_current_context`, `BaseTool`, `FunctionTool`, `tool`, and `PluginExecutionBridge` from `yasin_core.sdk`.

A fallback implementation exists for standalone/mock environments when `yasin_core` is unavailable.

## Concrete Execution Direction

`YasinCoreAgentAdapter` subclasses Core's `BaseAgent` and receives a `YasinCoreClient`. During execution it:

1. Builds a Core context.
2. Stores client, agent name, goal, execution history, shared variables, and task metadata in that context.
3. Renders AgentDefinition prompts/profile/config into the context.
4. Enters Core's `active_context`.
5. Builds an `agent_platform.task.Task`.
6. Plans steps through the local `TemplatePlanner`.
7. Executes those steps through the local `AgentExecutor` and `ToolRunner`.
8. Writes step results back into the Core context.
9. Returns the local executor's output or raises on failure.

## Critical Boundary Finding

The direction is not simply `Core executes Agent`. It is a hybrid integration model:

```text
Yasin-Core
  provides runtime contract + context + BaseAgent + client + SDK
                 ↓
Yasin-Agent adapter
  translates AgentDefinition into Core BaseAgent
                 ↓
Yasin-Agent local planner/executor/tool system
  performs application-level workflow execution
                 ↓
Core context / memory / registration surfaces
```

Core owns the runtime-facing contract and composition boundary; Yasin-Agent owns the domain-level workflow execution implementation.

## Memory Boundary

`save_agent_memory()` and `get_agent_memory()` resolve the active Core client from the current Core context and delegate to the client's memory methods.

This establishes:

- Core: memory infrastructure/runtime API;
- Agent: application-level use and session/context semantics.

## Tool Boundary

`register_all_agents()` can register ToolRunner tools into the Core client, wrapping plain callables as Core `FunctionTool` objects when required.

```text
Agent ToolRunner
      ↓
Core FunctionTool / BaseTool
      ↓
YasinCoreClient
```

## Plugin Boundary

The integration module imports `PluginExecutionBridge` and its fallback provides plugin discovery/registration behavior. Plugin ownership still requires deeper inspection.

## ADR Impact

| ADR | Result | Action |
|---|---|---|
| ADR-0003 | **CONFIRMED with precise boundary** | Describe hybrid Core runtime contract + Agent application workflow |
| ADR-0008 | **PARTIAL** | Core owns memory/storage primitives; Agent owns application context/session semantics |
| ADR-0007 | **UNVERIFIED** | Provider ownership is not established by this pass |
| ADR-0006 | **PARTIAL** | Agent CLI does not establish ecosystem-wide CLI ownership |

## Architectural Decision Update

Yasin-Agent should compose higher-level agent definitions, workflow planning, tools, sessions, and application semantics on top of Core rather than duplicating Core runtime services where a Core SDK contract exists.

## Remaining Verification

- dependency/package metadata;
- planner/executor tests;
- memory/session implementation details;
- plugin integration tests;
- CLI integration details;
- exact Core SDK version compatibility.

The Core↔Agent relationship is now concrete enough to update the ecosystem dependency graph, while final ADR acceptance remains dependent on cross-project verification and maintainer review.
