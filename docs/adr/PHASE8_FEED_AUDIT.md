# Phase 8 — YasinFeed Source Audit

- Date: 2026-08-11
- Status: Source-verified baseline
- Repository: `yusi20006-max/Yasinfeed`
- Scope: collection, processing/rewrite, scheduling, storage, publishing, API, and ecosystem boundaries

## Executive Finding

YasinFeed is an application-level content pipeline. Its documented implementation boundary is intentionally narrower than YasinHub, Yasin-Agent, and YasinCLI: it owns collection, article processing/rewrite, persistence, scheduling, and delivery adapters, while explicitly excluding ecosystem orchestration, agent decision-making, and CLI lifecycle management.

## Verified Pipeline

```text
Feed Sources
    ↓
fetch
    ↓
models / Article
    ↓
rewrite / processing
    ↓
storage
    ↓
publisher
 ┌──┼───────────┐
 ↓  ↓           ↓
Eitaa RSS       PWA/API

scheduler
    ↓
repeats fetch → process → store → publish
```

The repository README explicitly identifies `fetch`, `rewrite`, `storage`, `scheduler`, `publisher`, `models`, `api`, and `engine` as the application modules and describes a default `fetch_and_process` automation pipeline.

## Ownership Classification

| Capability | Current owner | Classification | Evidence status |
|---|---|---|---|
| Feed/source collection | YasinFeed | `RUNTIME_DEPENDENCY` internal | CONFIRMED |
| Article model/schema | YasinFeed | `DATA/SCHEMA_DEPENDENCY` internal | CONFIRMED |
| Rewrite/summarization boundary | YasinFeed | `OPTIONAL_INTEGRATION` / adapter boundary | CONFIRMED |
| SQLite/file persistence | YasinFeed | `DATA/SCHEMA_DEPENDENCY` internal | CONFIRMED |
| Scheduling | YasinFeed | runtime/application service | CONFIRMED |
| Eitaa publishing | YasinFeed | external delivery integration | CONFIRMED |
| RSS output | YasinFeed | external/content output | CONFIRMED |
| PWA JSON output | YasinFeed | API/output boundary | CONFIRMED |
| YasinHub orchestration | — | explicitly excluded from Feed | CONFIRMED |
| Yasin-Agent workflow execution | — | explicitly excluded from Feed | CONFIRMED |
| YasinCLI lifecycle control | — | explicitly excluded from Feed | CONFIRMED |
| Yasin-Core runtime | — | no audited direct dependency established | UNVERIFIED |
| Yasin-AI platform | — | no audited direct dependency established | UNVERIFIED |

## Important Boundary Finding

YasinFeed's README says its scheduler registers a `fetch_and_process` job that performs fetching, article creation/storage, rewriting, and publishing. Therefore scheduling is currently part of the Feed application's execution layer.

This does **not** mean YasinFeed owns ecosystem-level orchestration. The repository explicitly separates:

- YasinFeed → application pipeline execution;
- YasinHub → service management/system coordination;
- Yasin-Agent → agent workflows and decision-making;
- YasinCLI → user-facing lifecycle control.

This distinction should remain explicit in the canonical architecture.

## AI Boundary

The rewrite module is described as supporting standard/AI summary layers and future LLM adapters such as Ollama, OpenAI, and Claude. The repository also explicitly says heavy AI models and agent frameworks should not be integrated directly into the core application.

Therefore the current evidence supports an **AI adapter boundary owned by YasinFeed**, not a confirmed runtime dependency on Yasin-AI.

## Relay Comparison Impact

The YasinRelay audit confirms that Relay also owns a complete content pipeline ending in Eitaa publishing. YasinFeed independently owns a collection → process → store → publish pipeline with Eitaa/RSS/PWA outputs.

This is not sufficient evidence that one project should replace the other. It does establish real responsibility overlap that must be represented as either:

1. intentionally specialized application pipelines, or
2. a future shared pipeline/platform extraction.

No consolidation should be recorded as an accepted architecture decision without additional evidence and an explicit ADR.

## ADR Impact

- ADR-0006: **CONFIRMED at application-boundary level**; Feed owns its content pipeline and does not own ecosystem orchestration.
- ADR-0008: **PARTIAL**; Feed-local storage is confirmed, but ecosystem-wide memory/storage ownership remains unresolved.
- ADR-0010: **CONFLICT/OPEN REVIEW** until the Feed/Relay overlap is explicitly modeled.

## Evidence Gaps

1. Direct source verification of the scheduler, engine, and publisher implementations beyond the repository-level architecture description.
2. Package/import verification for Core, Agent, Hub, and AI integrations.
3. Comparison with YasinPress to determine whether Press is a specialized Feed derivative or an independently owned pipeline.
4. Final ownership decision for shared content-processing abstractions.

## Next Step

Audit YasinPress at source level. Then produce a Feed ↔ Relay ↔ Press comparison and update ADR-0010 plus the ecosystem dependency matrix.