# Yasin Ecosystem — Public API & Symbol-Level Graph

**Phase:** 6 — System Graphs  
**Status:** Refinement pass 6

## 1. Purpose

This document defines the current public-symbol evidence for the ecosystem. It separates:

- public API;
- internal implementation symbols;
- documented integration points;
- conceptual capabilities.

A symbol is **not** considered public merely because it exists in source code. Public status requires an export, documented import path, stable SDK surface, CLI contract, or explicit project documentation.

## 2. Yasin-Core Public Surface

Repository documentation identifies the public SDK boundary as:

```text
yasin_core.sdk
├── public SDK clients
├── interfaces
├── models
└── compatibility helpers
```

The repository also explicitly identifies these major internal/public-capability namespaces:

```text
yasin_core.agents
yasin_core.api
yasin_core.compatibility
yasin_core.config
yasin_core.context
yasin_core.core
yasin_core.di
yasin_core.events
yasin_core.execution
yasin_core.memory
yasin_core.observability
yasin_core.plugins
yasin_core.providers
yasin_core.runtime
yasin_core.sdk
yasin_core.security
yasin_core.storage
```

The README describes `yasin_core.sdk` as the public SDK surface, while the other namespaces provide runtime capabilities. fileciteturn40file0

## 3. Verified Cross-Project Core Symbol

Yasin-Agent documentation explicitly uses:

```python
from yasin_core.sdk import YasinCoreClient
```

Therefore:

```text
Yasin-Agent
   │
   └── consumes → yasin_core.sdk.YasinCoreClient
```

This is currently the strongest documented symbol-level cross-project contract.

## 4. Yasin-Agent Public Boundary

Documented integration symbols include:

```text
YasinCoreClient
YasinCoreAgentAdapter
register_cli_command
```

Documented CLI contract:

```text
python -m agent_platform.cli agent run <agent_name>
```

The Agent repository also documents these major modules:

```text
agent_definition
agent_registry
task
state_machine
planner
executor
tool_runner
memory_context
integration
cli
```

These module names are architecture evidence; they are not automatically public APIs.

## 5. Yasin-AI Public Boundary

The repository defines Yasin-AI as a modular AI platform with boundaries for:

```text
Runtime
API / Services
Knowledge / Retrieval
Persistent Memory
Developer / Plugins
Observability
Deployment / Infrastructure
```

The documented persistence contract is specifically:

```text
Local SQLite-backed storage
```

and the plugin boundary is explicitly trusted/in-process. Remote untrusted plugin execution is not currently supported. fileciteturn41file0

Exact class/function exports require source-level symbol inspection before being promoted to the stable public API registry.

## 6. YasinHub Public Boundary

YasinHub documents these concrete integration symbols:

```python
from yasinhub.status_store import write_status

write_status("yasinrelay", success=True, message="...")
```

and the CLI contract:

```text
python3 -m yasinhub.cli status
```

Its documented internal modules are:

```text
status_store
process_checker
registry
report
cli
```

`write_status()` is therefore a documented producer-side integration point for status reporting. fileciteturn42file0

## 7. YasinRelay Public Boundary

The documented operational CLI surface includes:

```text
python3 -m yasinrelay.cli run
python3 -m yasinrelay.cli run --limit N
python3 -m yasinrelay.cli run --channel <channel>
python3 -m yasinrelay.cli run --schedule
python3 -m yasinrelay.cli run --loop
```

Its documented internal boundaries include:

```text
storage
pipeline_engine
ai_processor
media_processor
logging_config
scheduler
pipeline
cli
```

The documented environment contract includes database path, source channels, publishing credentials, AI provider/base URL/model, and scheduling settings. fileciteturn43file0

The README also documents an internal Agent platform with `LifecycleHooks` and `EventBus`; these must be treated as Relay-local APIs unless an independent cross-project contract is established. fileciteturn43file0

## 8. Public API Classification Matrix

| Project | Verified public boundary | Confidence |
|---|---|---|
| Yasin-Core | `yasin_core.sdk` / `YasinCoreClient` | High |
| Yasin-Agent | `YasinCoreAgentAdapter`, `YasinCoreClient`, CLI integration | High/documented |
| Yasin-AI | Runtime/service/plugin boundaries; exact exports pending | Medium |
| YasinHub | `write_status()`, status CLI | High/documented |
| YasinRelay | CLI commands; pipeline/agent interfaces documented | High/documented |
| YasinFeed | Architecture-level boundary pending source symbol audit | Medium |
| YasinPress | Architecture-level boundary pending source symbol audit | Medium |
| YasinCLI | CLI command surface pending exact symbol audit | Medium |

## 9. API Ownership Model

Every stable cross-project API should eventually have:

```text
Producer repository
Module
Symbol
Input schema
Output schema
Error semantics
Version policy
Compatibility policy
Consumer repositories
Deprecation policy
```

## 10. API Stability Levels

Use the following labels:

```text
STABLE
  Explicitly public and versioned/documented.

DOCUMENTED
  Public integration is documented but formal compatibility policy may be incomplete.

INTERNAL
  Implementation detail; consumers must not depend on it.

CONCEPTUAL
  Architecture capability only; no concrete symbol contract.

UNKNOWN
  Evidence insufficient.
```

## 11. Important Boundary Rules

### Core
Other repositories should consume Core through its SDK/compatibility boundaries rather than importing private implementation modules.

### Agent
Agent orchestration internals (`planner`, `executor`, `state_machine`, etc.) should remain internal unless explicitly exported.

### Hub
Status reporting is a producer contract. Hub's internal storage/reporting implementation is not automatically an API for other projects.

### Relay
Pipeline stages are implementation boundaries unless explicitly exposed through a stable package API.

### AI
Plugin interfaces are trusted in-process boundaries. They must not be interpreted as a remote execution API.

## 12. Symbol-Level Verification Gaps

The following still require direct source inspection:

- `yasin_core.sdk` exact exports and `__all__`;
- exact `YasinCoreClient` methods/signatures;
- Agent adapter method signatures;
- Hub `write_status()` schema and persistence contract;
- Relay pipeline-stage interfaces and event payload classes;
- YasinFeed public classes/functions;
- YasinPress public classes/functions;
- YasinCLI command registry and adapter interfaces;
- package-level re-exports;
- deprecation/version guarantees.

## 13. Rule for Future AI Agents

Before using a symbol across repositories:

1. locate the symbol in source;
2. verify its import path;
3. verify export/re-export status;
4. inspect signature/schema;
5. inspect tests or documented usage;
6. classify stability;
7. record the dependency in YASIN-DOCS.

Never turn a convenient internal import into an ecosystem contract without an explicit architectural decision.
