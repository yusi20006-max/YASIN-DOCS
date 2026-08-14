# Yasin Projects

This document is the current **repository registry**. It is based on repository metadata, repository files, and source/runtime verification.

> **Evidence rule:** repository metadata, repository files, and executed verification are authoritative for implementation claims. A project is not considered part of the core Yasin architecture merely because its name contains `Yasin`.

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
| `YasinCoder` | **Canonical coding-agent application; local/cloud AI provider gateway and coding workflows** | `master` | Public | Phase 1/2 runtime verification on 2026-08-14 |
| `YASIN-DOCS` | Central ecosystem architecture/documentation hub | `main` | Public | This repository |

## Related / Supporting Repositories

| Repository | Verified role | Default branch | Visibility | Relationship |
|---|---|---:|---|---|
| `Openfeed` | Stable Go Telegram public-channel fetcher + local API/PWA | `main` | Public | Fetching foundation referenced by FeedBridge/YasinRelay history |
| `Feedbridge` | Self-contained Telegram content bridge with AI and Eitaa publishing | `main` | Public | Downstream content bridge; embeds OpenFeed-derived fetcher |
| `TJC` | Termux/Jules workflow and scheduler CLI | `main` | Public | Developer automation tooling |
| `Termux-BackupManager` | Termux backup/restore/migration tooling | `main` | Public | Developer/operations tooling |
| `YasinJules` | Jules-related repository | `jules-2685192485704646500-c69dfdb7` | Public | Requires deeper audit before architectural classification |
| `Yasinpress` | Automated Persian news collection/AI processing/Eitaa publishing application | `main` | Private | Legacy/domain application; relationship to Rewrite requires evidence |
| `YasinPress-Rewrite-` | Production-oriented Python news collection, processing and publishing application | `main` | Private | Verified runnable baseline; 1.0.0; 114 tests pass |

## YasinCoder — Current Architectural Record

YasinCoder is now classified as the **canonical coding-agent repository**. The implementation and local/cloud provider integration work should converge there rather than being split across separate coding-agent repositories.

Verified local stack:

```text
YasinCoder
   │
   ├── Agent / project intelligence / command modules
   │
   └── AI provider layer
          │
          ├── Local gateway :18765
          │      └── llama-server :18080
          │             └── Qwen3 1.7B Q4_K_M
          │
          └── Gemini CLI
```

The 2026-08-14 verification established a working offline Qwen path, lifecycle controls, UI HTTP 200, status/log APIs, and successful `/api/qwen` generation. Gemini CLI availability was confirmed, but the configured `gemini-3.5-flash` account was quota-exhausted and returned HTTP 429 during generation.

Detailed records:

- [`YasinCoder Architecture & Roadmap`](docs/projects/yasincoder/ARCHITECTURE-ROADMAP.md)
- [`YasinCoder Phase 2 AI Integration Audit`](docs/projects/yasincoder/PHASE2-AI-INTEGRATION-AUDIT.md)

## Important Findings

### 1. Yasin-Core is the clearest foundation boundary
The current README describes Yasin-Core as the central runtime layer covering agents, API, compatibility, configuration, context, execution, memory, observability, plugins, providers, runtime, SDK, security, and storage.

### 2. Yasin-Agent has a duplicated/transitioning identity
Its README describes `agent_platform` as a Yasin-AI component and says it provides the agent/workflow/tool/memory/context layer plus a Yasin-Core SDK adapter. Deeper source-level audit is still required before declaring the final boundary.

### 3. Yasin-AI is the broader shared AI platform
The ecosystem documentation defines Yasin-AI as the canonical owner of shared ecosystem-wide AI capabilities while preserving independent runtime ownership and requiring explicit public/versioned contracts.

### 4. YasinHub is currently small and concrete
It is a status-oriented CLI/store and should not be described as a full orchestration platform without source-level evidence.

### 5. YasinRelay is a complete content pipeline
Its documented pipeline is Collector → Normalizer → Validator → Duplicate Detection → AI Processor → Media Preparation → Publisher.

### 6. YasinFeed explicitly enforces boundaries
Its README assigns collection/processing/publishing to Feed, service coordination to YasinHub, agent workflows to Yasin-Agent, and CLI behavior to YasinCLI. These statements require continued source validation.

### 7. YasinCLI is a control-plane candidate
The repository documents configuration, commands, doctor diagnostics, status, service management and plugins. Its non-main default branch requires care before production classification.

### 8. OpenFeed and FeedBridge have explicit lineage
OpenFeed is a stable fetching core; FeedBridge documents a vendored fetcher derived from OpenFeed's `telemirror` engine. Exact historical relationships with YasinRelay require source/history audit.

### 9. YasinPress Rewrite is source/runtime verified
A fresh Termux installation passed the complete test suite (`114 passed`) and verified CLI/database/config health. Live publishing remains pending fresh credential verification.

### 10. Yasinnews is not currently verified
A repository lookup returned no matching repository under the audited account.

## Next Registry Upgrade

Maintain canonical repository URL, category, lifecycle, owner, dependencies, consumers, interfaces, stores, external integrations, evidence level, and cross-project impact. Detailed project records remain under `docs/projects/`.
