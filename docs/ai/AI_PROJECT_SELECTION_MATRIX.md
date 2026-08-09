# AI Project Selection Matrix

## Goal

Choose the repository that owns a requested change before editing.

| Request area | Primary repo | First evidence to inspect | Likely impact |
|---|---|---|---|
| runtime abstractions | Yasin-Core | `yasin_core/`, SDK, runtime tests | Agent/consumers |
| agent/task execution | Yasin-Agent | agent modules, Core adapter, tests | Core |
| model/provider/knowledge | Yasin-AI | provider, retrieval, memory modules | Agent/Relay consumers where integrated |
| status/management | YasinHub | status store, CLI, management modules | CLI/runtime |
| ingestion/relay/pipeline | YasinRelay | pipeline, storage, scheduler, processors | publishing/AI |
| feed generation/publishing | YasinFeed | fetch/rewrite/storage/publisher | downstream publishing |
| news/press | YasinPress | processing/publishing modules | content consumers |
| unified operator CLI | YasinCLI | command registry/adapters | managed components |
| Jules/developer automation | TJC | command/adapters/workflows | development process |
| architecture/docs | YASIN-DOCS | architecture/AI docs/registry | ecosystem knowledge |

## Decision Procedure

```text
User request
  ↓
Classify behavior
  ↓
Find owner
  ↓
Check documented consumers
  ↓
Inspect source
  ↓
Confirm ownership
  ↓
Edit
```

## Ambiguous Requests

If multiple repositories appear relevant, do not choose based on name alone. Determine whether the requested behavior is:

- owned implementation;
- consumed API;
- orchestration;
- documentation;
- configuration;
- deployment.

Change the owner, not merely the first consumer encountered.

## Multi-Repository Changes

A cross-repository change is required when a public contract changes. Record all affected repositories and validate each consumer.
