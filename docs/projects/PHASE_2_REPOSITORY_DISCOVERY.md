# Phase 2 — Repository Discovery

**Audit date:** 2026-08-09  
**Scope:** GitHub repositories accessible under `yusi20006-max`

## Objective

Establish a verified inventory of the Yasin ecosystem before writing the final master architecture. This phase intentionally separates repository evidence from historical assumptions and planned architecture.

## Evidence Model

Each classification has one of these meanings:

- **Verified:** directly supported by repository metadata or current repository documentation.
- **Provisional:** plausible from repository naming/history but requires source-level confirmation.
- **Not found:** no repository matching the expected name was found in the audited account.
- **Out of scope:** visible repository that is not currently classified as a Yasin ecosystem component.

## Repository Inventory

### Verified core ecosystem

#### Yasin-Core

- Repository: `yusi20006-max/Yasin-core`
- Default branch: `main`
- Visibility: public
- Documented version: `3.3.0`
- Role: central runtime/foundation layer
- Major documented areas: agents, API, compatibility, config, context, core lifecycle, dependency injection, events, execution, memory, observability, plugins, providers, runtime, SDK, security, storage.
- Release state: release-freeze validation for v3.3.0.
- Key architectural observation: this is currently the strongest candidate for the ecosystem foundation boundary.

#### Yasin-Agent

- Repository: `yusi20006-max/Yasin-agent`
- Default branch: `main`
- Visibility: public
- Documented version: `1.0.0 stable`
- Role: agent definition, workflow/planning, execution, tools, plugins, sessions, memory/context integration, and Yasin-Core SDK adaptation.
- Key architectural observation: README describes `agent_platform` as a Yasin-AI component while this repository separately hosts it. Source-level inspection is required to settle packaging and ownership boundaries.

#### Yasin-AI

- Repository: `yusi20006-max/Yasin-AI`
- Default branch: `main`
- Visibility: public
- Documented version: `1.1.0`
- Role: production-oriented modular AI platform.
- Major boundaries: runtime orchestration, API/service layer, knowledge/retrieval, persistent memory, developer/plugin platform, observability, deployment, security.
- Documented limitations: local SQLite persistence by default; no distributed HA storage; trusted in-process plugin execution; no untrusted remote plugin sandboxing.

#### YasinHub

- Repository: `yusi20006-max/YasinHub`
- Default branch: `main`
- Visibility: public
- Role: lightweight status/health reporting tool.
- Major modules: status store, process checker, project registry, report generator, CLI.
- Current behavior: projects write JSON status and Hub combines status with live process checks.
- Boundary warning: do not currently treat Hub as a full orchestration/control platform without source evidence.

#### YasinRelay

- Repository: `yusi20006-max/YasinRelay`
- Default branch: `main`
- Visibility: public
- Documented version: `2.0.0 stable`
- Role: content relay pipeline from Telegram sources through normalization, validation, deduplication, AI processing, media preparation, and Eitaa publishing.
- Major infrastructure: SQLite storage, scheduler, structured logging, configuration, Go fetcher, Python pipeline/CLI.
- Key boundary: content transport/processing/publishing rather than ecosystem-wide management.

#### YasinFeed

- Repository: `yusi20006-max/Yasinfeed`
- Default branch: `main`
- Visibility: public
- Role: modular content collection, processing, output preparation, and publishing engine.
- Modules: API, fetch, models, publisher, rewrite, scheduler, storage, config, logging, engine.
- Explicit documented exclusions: it is not YasinHub, Yasin-Agent, or YasinCLI.
- Key architectural observation: its README explicitly defines cross-project boundaries, making it valuable evidence for the master architecture.

#### YasinCLI

- Repository: `yusi20006-max/Yasin-cli`
- Default branch: `initial-setup`
- Visibility: public
- Role: Node.js cross-platform CLI/control-plane candidate.
- Major modules: config manager, command framework/registry, doctor, status, service manager, plugin system.
- Platforms documented: Termux/Android, Linux, macOS, Windows.
- Key architectural observation: current repository branch state must be included in production-status assessment.

#### YASIN-DOCS

- Repository: `yusi20006-max/YASIN-DOCS`
- Default branch: `main`
- Visibility: public
- Role: system-level documentation, architecture, decisions, project registry, AI handoff, and ecosystem knowledge source.

## Verified related projects

### OpenFeed

- Repository: `yusi20006-max/Openfeed`
- Default branch: `main`
- Role: Go-based public Telegram channel fetcher with local API and PWA.
- Architecture: Go server, `telemirror` fetching engine, provider/parser/model/API layers, and lightweight web PWA.
- Documented policy: stable core; new AI/scheduling/publishing/dashboard/plugin features should live downstream.

### FeedBridge

- Repository: `yusi20006-max/Feedbridge`
- Default branch: `main`
- Role: self-contained Telegram content bridge with embedded OpenFeed-derived fetcher, duplicate detection, AI, queue, publishing, dashboard, plugins, and health monitoring.
- Key relationship: embeds a vendored fetcher derived from OpenFeed's `telemirror` engine rather than requiring OpenFeed at runtime.
- Architectural question: determine whether this repository is legacy, experimental, or still an active component of the intended Yasin architecture.

### TJC

- Repository: `yusi20006-max/TJC`
- Default branch: `main`
- Role: POSIX-shell/Termux CLI for Google Jules API workflows.
- Major systems: workflow engine, scheduler, plugins/extensions, reports, testing and development tooling.
- Classification: developer automation/supporting tooling, not runtime core.

### Termux-BackupManager

- Repository: `yusi20006-max/Termux-BackupManager`
- Default branch: `main`
- Role: Termux backup/restore/migration utility.
- Dependencies documented: Termux, rclone, Google Drive remote.
- Classification: operations/supporting tooling.

## Private Yasin repositories

### Yasinpress

- Repository: `yusi20006-max/Yasinpress`
- Default branch: `main`
- Visibility: private
- Documented version: `2.0.0`
- Role: automated Persian news collection and Eitaa publishing application.
- Major capabilities: RSS collection, duplicate detection, categorization, optional Cloudflare Workers AI processing, daily digest, queueing, rate limiting, SQLite, process locking, and Eitaa publishing.
- Architectural caution: substantial overlap exists with YasinFeed/YasinRelay; source-level comparison is required before assigning final ownership.

### YasinPress-Rewrite-

- Repository: `yusi20006-max/YasinPress-Rewrite-`
- Default branch: `main`
- Visibility: private
- Current role: rewrite-related YasinPress repository; requires deeper audit.

## Repositories requiring deeper classification

### YasinJules

- Public repository.
- Default branch: `jules-2685192485704646500-c69dfdb7`.
- Requires source/history inspection before being classified as a stable ecosystem component.

### YasinCoder

- Public repository.
- Default branch: `master`.
- Requires source/history inspection before being classified as a stable ecosystem component.

## Not currently verified

### Yasinnews

No repository matching `Yasinnews` was found in the audited account. It must not be added to the architecture as an active repository until a canonical repository is identified.

## Other visible account repositories

These are currently excluded from the Yasin ecosystem architecture unless later evidence establishes a direct architectural relationship:

- `bpb-worker-panel`
- `Nova-Proxy`
- `hermes-webui`
- `hermes-agent-mobile`
- `Telegram-Mirror`

## Cross-Project Questions Generated by Phase 2

1. Is `Yasin-Agent` an independent product boundary or a separately packaged component extracted from `Yasin-AI`?
2. What exact APIs/contracts connect Yasin-Core to Yasin-Agent, YasinHub, YasinRelay, and YasinCLI?
3. Is YasinHub intentionally a status/health tool only, or is orchestration planned elsewhere?
4. What is the intended relationship between YasinFeed, YasinRelay, FeedBridge, OpenFeed, and YasinPress?
5. Which content pipeline is canonical for the current Yasin architecture?
6. Which repositories are active products versus historical/experimental/transition repositories?
7. Which project owns AI provider abstraction: Yasin-Core, Yasin-AI, or downstream adapters?
8. Which project owns persistent memory versus context versus knowledge retrieval?
9. Which project owns lifecycle/process management versus reporting/health?
10. What is the intended final role of YasinCLI as the ecosystem control plane?

These questions become the input to Phase 3 and the detailed source-level audit in Phase 5.
