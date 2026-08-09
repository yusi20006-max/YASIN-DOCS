# Yasin Projects

This document is the current **Phase 2 repository registry**. It is based on the repositories visible in the GitHub account audit performed for YASIN-DOCS on 2026-08-09.

> **Evidence rule:** repository metadata and repository files are authoritative for implementation claims. A project is not considered part of the core Yasin architecture merely because its name contains `Yasin`.

## Core / Ecosystem Repositories

| Repository | Verified role | Default branch | Visibility | Current evidence |
|---|---|---:|---|---|
| `Yasin-core` | Shared runtime/foundation layer | `main` | Public | README v3.3.0 |
| `Yasin-agent` | Agent/workflow execution platform | `main` | Public | README v1.0.0 |
| `Yasin-AI` | Modular AI platform/runtime services | `main` | Public | README v1.1.0 |
| `YasinHub` | Lightweight status/health aggregation CLI | `main` | Public | README |
| `YasinRelay` | Content relay pipeline: fetch → process → publish | `main` | Public | README v2.0.0 |
| `Yasinfeed` | Content collection, processing, and publishing engine | `main` | Public | README |
| `Yasin-cli` | Cross-platform Node.js control/diagnostic CLI | `initial-setup` | Public | README |
| `YASIN-DOCS` | Central ecosystem architecture/documentation hub | `main` | Public | This repository |

## Related / Supporting Repositories

| Repository | Verified role | Default branch | Visibility | Relationship |
|---|---|---:|---|---|
| `Openfeed` | Stable Go Telegram public-channel fetcher + local API/PWA | `main` | Public | Fetching foundation referenced by FeedBridge/YasinRelay history |
| `Feedbridge` | Self-contained Telegram content bridge with AI and Eitaa publishing | `main` | Public | Downstream content bridge; embeds OpenFeed-derived fetcher |
| `TJC` | Termux/Jules workflow and scheduler CLI | `main` | Public | Developer automation tooling |
| `Termux-BackupManager` | Termux backup/restore/migration tooling | `main` | Public | Developer/operations tooling |
| `YasinJules` | Jules-related repository | `jules-2685192485704646500-c69dfdb7` | Public | Requires deeper audit before architectural classification |
| `YasinCoder` | Yasin coding-related repository | `master` | Public | Requires deeper audit before architectural classification |
| `Yasinpress` | Automated Persian news collection/AI processing/Eitaa publishing application | `main` | Private | Domain application; separate from YasinFeed until boundaries are verified |
| `YasinPress-Rewrite-` | YasinPress rewrite-related repository | `main` | Private | Requires deeper audit |

## Other Account Repositories

The account also contains projects that are not currently classified as Yasin ecosystem components:

- `bpb-worker-panel`
- `Nova-Proxy`
- `hermes-webui`
- `hermes-agent-mobile`
- `Telegram-Mirror`

These are recorded separately so the ecosystem audit does not accidentally absorb unrelated infrastructure or experiments.

## Important Findings From Phase 2

### 1. Yasin-Core is the clearest foundation boundary

The current README explicitly describes Yasin-Core as the central runtime layer and lists agents, API, compatibility, configuration, context, execution, memory, observability, plugins, providers, runtime, SDK, security, and storage as major areas.

### 2. Yasin-Agent currently has a duplicated/transitioning identity

Its README describes `agent_platform` as a Yasin-AI component and says it provides the agent/workflow/tool/memory/context layer plus a Yasin-Core SDK adapter. This needs a deeper source-level audit before declaring whether Yasin-Agent is a fully independent runtime boundary or a separately packaged component of Yasin-AI.

### 3. Yasin-AI is a broader application/runtime platform

The README identifies runtime orchestration, API/services, knowledge/retrieval, persistent memory, developer/plugin interfaces, observability, deployment, and security as its boundaries. It explicitly states that plugin execution is trusted and in-process and that distributed HA storage and untrusted remote plugin sandboxing are not currently supported.

### 4. YasinHub is currently small and concrete

The current implementation is a status-oriented CLI/store: projects report status, a process checker checks live processes, a registry defines monitored projects, and a report combines status and process information. It should not currently be documented as a full orchestration platform without source-level evidence.

### 5. YasinRelay is a complete content pipeline

The documented pipeline is Collector → Normalizer → Validator → Duplicate Detection → AI Processor → Media Preparation → Publisher. It has SQLite storage, deduplication, scheduling, structured logging, configuration, a Go fetcher, and Eitaa publishing.

### 6. YasinFeed explicitly enforces boundaries

Its README states that it owns collection, processing, and publishing pipes, while YasinHub owns service management/coordination, Yasin-Agent owns agent workflows/decision-making/automation, and YasinCLI owns CLI behavior. These statements will be validated against code in the detailed audit.

### 7. YasinCLI is currently a Node.js control-plane candidate

The repository documents configuration management, command registry, doctor diagnostics, status, service management, and plugins. Its default branch is currently `initial-setup`, so branch/version history must be considered before declaring it production-ready.

### 8. OpenFeed and FeedBridge have an explicit lineage

OpenFeed documents itself as a stable fetching core. FeedBridge documents a vendored fetcher derived from OpenFeed's `telemirror` engine and adds processing, AI, queueing, publishing, dashboard, plugins, and health monitoring. YasinRelay also documents a Go fetcher and a broader relay pipeline. The exact historical and current relationship among these repositories requires source/history audit before consolidation decisions.

### 9. Yasinnews is not currently present under the audited GitHub account

A repository lookup for `Yasinnews` returned no matching repository. It must therefore be treated as **not verified/present** rather than assumed to exist.

## Next Registry Upgrade

Phase 3 will convert this inventory into a machine-readable registry with:

- canonical repository URL;
- project category;
- lifecycle status;
- owner responsibility;
- dependencies;
- consumers;
- interfaces;
- data stores;
- external integrations;
- implementation confidence/evidence level;
- cross-project impact.

Phase 5 will then create the detailed architecture record for each confirmed ecosystem project.
