# Phase 8 — Yasin-Core ↔ Yasin-Agent Dependency Graph

- Date: 2026-08-09
- Status: Source-verified draft
- Repositories: `yusi20006-max/Yasin-core`, `yusi20006-max/Yasin-agent`

## Executive Finding

The Core↔Agent relationship is a layered hybrid integration. Yasin-Agent is an API consumer of Yasin-Core, but it retains local application-level planning and execution components.

## Verified Dependency Graph

```text
                         YASIN-CORE
                             │
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
          BaseAgent       Context        YasinCoreClient
              │              │              │
              └──────────────┼──────────────┘
                             ↓
                    YASIN-AGENT INTEGRATION
                             │
                  YasinCoreAgentAdapter
                             │
          ┌──────────────────┼──────────────────┐
          ↓                  ↓                  ↓
   AgentDefinition      TemplatePlanner     ToolRunner
                               │                  │
                               ↓                  ↓
                         AgentExecutor      Core Tools
                               │                  │
                               └────────┬─────────┘
                                        ↓
                                  Task Context
                                        │
                                        ↓
                              Core Memory / Context
```

## Dependency Classification

| Edge | Type | Direction | Meaning |
|---|---|---|---|
| Agent → Core SDK | `API_DEPENDENCY` | Agent → Core | Imports public SDK types and client |
| Adapter → BaseAgent | `RUNTIME_DEPENDENCY` | Agent → Core | Adapter subclasses Core agent primitive |
| Adapter → Core Context | `API_DEPENDENCY` | Agent → Core | Uses active context/context creation |
| Agent → Core Memory | `API_DEPENDENCY` | Agent → Core | Delegates memory operations through client |
| Agent ToolRunner → Core Tool API | `API_DEPENDENCY` | Agent → Core | Resolves/executes Core-registered tools |
| Agent Planner → Agent Executor | `INTERNAL` | Agent | Local workflow pipeline |
| Agent Executor → ToolRunner | `INTERNAL` | Agent | Local step execution |
| Agent → Core Plugins | `OPTIONAL_INTEGRATION` | Agent → Core | Plugin bridge exists |

## Responsibility Split

### Yasin-Core owns

- runtime composition;
- reusable agent runtime primitives;
- `BaseAgent` contract;
- Core context/runtime context;
- SDK client;
- memory/storage infrastructure;
- provider infrastructure;
- Core tool abstractions and registration;
- security and lifecycle services;
- ecosystem compatibility mechanisms.

### Yasin-Agent owns

- Agent definitions/profiles;
- application-level agent behavior;
- template-based planning;
- task model/state semantics at Agent layer;
- sequential workflow execution;
- retry/step validation behavior;
- local tool registry/dispatch;
- Agent-facing sessions and workflow semantics;
- translation between Agent concepts and Core runtime contracts.

## Important Implementation Evidence

`TemplatePlanner` currently uses pre-registered goal templates and returns independent `Step` copies. This means the current planner is deterministic/template-driven rather than an LLM planner. fileciteturn122file0

`Executor` performs sequential step execution, retries failed steps according to `max_retries`, validates outputs when a validator is configured, updates task context with step outputs, and transitions task state. fileciteturn123file0

`ToolRunner` maintains local callable registrations but can fall through to the active Core client, discover Core-registered tools, merge context into arguments, filter arguments against callable signatures, and execute the Core tool through `client.execute_tool()`. fileciteturn124file0

These facts prove that the Agent execution path is intentionally hybrid rather than a simple wrapper around Core execution.

## Architectural Rule

Yasin-Agent should extend and compose Core capabilities rather than reimplement Core infrastructure. Local implementations are justified where they represent Agent-level domain semantics, such as workflow templates, task semantics, or application-specific tool dispatch.

## Open Questions

1. Exact Core SDK version/package pinning in Agent metadata.
2. Whether Agent tests enforce the Core integration contract.
3. Whether all Agent memory/session operations ultimately delegate to Core.
4. Whether plugin execution is a stable contract or compatibility layer.
5. Whether the current standalone fallback is intended for production or only tests/development.

## ADR Status

- ADR-0003: **CONFIRMED — precise hybrid boundary**.
- ADR-0008: **PARTIAL — storage/memory ownership still needs ecosystem-wide mapping**.
- Agent/Core dependency direction: **CONFIRMED**.
- Target architecture: pending cross-project audit.
