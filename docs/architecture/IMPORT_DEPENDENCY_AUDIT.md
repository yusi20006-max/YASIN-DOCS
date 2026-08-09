# Yasin Ecosystem — Import-Level Dependency Audit

**Phase:** 6 — System Graphs  
**Status:** Source-evidence pass 1

## 1. Purpose

This document records import/package dependency evidence without converting documentation references into false dependency edges.

## 2. Yasin-Agent — Source-Backed Boundary

The repository README documents the Agent package as:

```text
agent_platform/
├── __init__.py
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

It explicitly documents an integration with:

```python
from yasin_core.sdk import YasinCoreClient
```

and the `YasinCoreAgentAdapter` integration layer. The README also demonstrates `YasinCoreClient()` with `create_task()` and `execute_task()`. fileciteturn36file0

### Verified/documented cross-project edge

```text
Yasin-Agent
    │
    │ documented SDK import/integration
    ▼
Yasin-Core SDK
    └── YasinCoreClient
```

### Important limitation

The GitHub code-search connector did not return source matches for `from yasin_`, `import yasin`, or `yasin_core.sdk` in the attempted repository search. Therefore this pass does **not** claim a complete line-by-line import graph. The README is sufficient to establish the documented integration boundary, but not sufficient to enumerate every import edge.

## 3. Internal Agent Module Graph

The README establishes these module responsibilities:

```text
agent_definition
      │
      ▼
agent_registry
      │
      ├── planner
      ├── tool_runner
      └── integration

planner ──► task / state_machine
executor ──► task / planner / tool_runner
memory_context ──► session/context/memory
cli ──► registry/planner/tool_runner
```

This is a **responsibility graph**, not a definitive Python import graph. Exact imports require source-file enumeration.

## 4. Other Yasin Projects

For Yasin-Core, Yasin-AI, YasinHub, YasinRelay, YasinFeed, and YasinPress, this pass does not promote a cross-project edge to `import dependency` without direct source evidence.

Existing architecture documents may describe integration, API, or runtime relationships; those remain classified according to their evidence level.

## 5. Dependency Classification

| Edge type | Meaning |
|---|---|
| `import dependency` | Direct source import evidence |
| `package dependency` | Manifest/package metadata evidence |
| `documented integration` | README/API documentation evidence |
| `runtime integration` | Process/API/subprocess evidence |
| `conceptual` | Architecture intent only |
| `unknown` | Insufficient evidence |

## 6. Negative-Evidence Rule

A failed code-search query does **not** prove that an import does not exist. Search-index coverage, generated files, vendored code, branch differences, and connector limitations can all produce false negatives.

Therefore:

```text
No search result
      ≠
No dependency
```

## 7. What a Future Complete Import Audit Must Do

For every scoped repository:

1. enumerate source files;
2. parse Python/JS/TS imports where applicable;
3. normalize relative and absolute imports;
4. resolve local-package ownership;
5. distinguish third-party from Yasin-owned modules;
6. compare imports against package manifests;
7. identify optional/test-only imports;
8. record circular dependencies;
9. generate a machine-readable dependency graph;
10. record evidence path and commit/ref for every edge.

## 8. Current Confidence

**High confidence:** Yasin-Agent → Yasin-Core SDK integration is explicitly documented. fileciteturn36file0

**Medium confidence:** internal Agent module responsibility relationships.

**Not established:** complete cross-repository import graph.

## 9. AI Maintenance Rule

Never delete an edge solely because a search query returned no result. Never add an `import dependency` edge solely because two projects share a name, capability, or README reference.
