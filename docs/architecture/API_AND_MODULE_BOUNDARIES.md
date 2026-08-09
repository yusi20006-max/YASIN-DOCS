# Yasin Ecosystem — API and Module Boundary Evidence

**Phase:** 6 — System Graphs  
**Status:** Refinement pass 2

## 1. Yasin-Agent Module Graph

The repository README exposes the following implementation modules:

```text
agent_platform/
├── agent_definition.py
├── agent_registry.py
├── task.py
├── state_machine.py
├── planner.py
├── executor.py
├── tool_runner.py
├── memory_context.py
├── integration.py
└── cli.py
```

The documented responsibilities are:

- `agent_definition.py` — agent metadata/config/profile/prompt handling;
- `agent_registry.py` — registration and discovery of agents;
- `task.py` — task/result structures;
- `state_machine.py` — task lifecycle state transitions;
- `planner.py` — workflow steps and planning;
- `executor.py` — sequential execution, validation and retry;
- `tool_runner.py` — dynamic tool registration/invocation;
- `memory_context.py` — context, memory and isolated sessions;
- `integration.py` — Yasin-Core SDK adapter and fallback layer;
- `cli.py` — agent CLI integration.

This is direct repository documentation evidence, not an inferred module graph. fileciteturn25file0

## 2. Yasin-Agent Public Integration Boundary

The README explicitly documents:

```python
from yasin_core.sdk import YasinCoreClient
```

and:

```text
YasinCoreAgentAdapter
```

The documented flow is:

```text
AgentRegistry
     │
     ├── agents
     ├── planner
     └── tool_runner
             │
             ▼
      YasinCoreClient
             │
             ├── create_task
             └── execute_task
```

This establishes a concrete integration contract at the documentation level. Exact imported symbols and source call graph remain a follow-up task.

## 3. Agent Runtime Boundary

The documented execution pipeline is:

```text
Agent Definition
      ↓
Agent Registry
      ↓
Planner
      ↓
Task / State Machine
      ↓
Executor
      ↓
Tool Runner
      ↓
Result / Validation / Retry
```

Memory and Context are a parallel runtime concern:

```text
Session
  ├── Context
  ├── Short-term Memory
  └── Long-term Memory
```

## 4. CLI Boundary

Yasin-Agent exposes:

```text
python -m agent_platform.cli agent run <agent_name>
```

and documents `register_cli_command(cli_app)` as an integration mechanism capable of attaching the `agent run` command to an existing CLI abstraction.

Therefore the CLI is an adapter boundary rather than the core execution layer.

## 5. Core API Boundary

The currently verified public reference is:

```text
Yasin-Core
└── yasin_core.sdk
    └── YasinCoreClient
```

The precise public symbol inventory must be obtained from Yasin-Core source and package exports before publishing a definitive API map.

## 6. Graph Confidence

**Verified/documented:**
- Yasin-Agent module names and responsibilities;
- Yasin-Core SDK import path referenced by Agent;
- `YasinCoreClient` usage;
- task creation/execution example;
- Agent CLI entry command;
- Agent/Core adapter existence.

**Not yet symbol-verified:**
- every exported Core SDK symbol;
- exact Agent import graph;
- Hub API symbols;
- CLI adapter implementation details;
- Relay HTTP/event API symbols.

## 7. Rule for Future AI Agents

Do not infer a cross-project Python import merely from a repository name or README mention. A definitive import edge requires source evidence.

Until then, label the edge `documented integration` rather than `package dependency`.
