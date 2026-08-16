# Yasin Projects

This document is the current **repository registry**. It is based on repository metadata, repository files, and source/runtime verification.

> **Evidence rule:** repository metadata, repository files, and executed verification are authoritative for implementation claims. A project is not considered part of the core Yasin architecture merely because its name contains `Yasin`.

> **Phase 0 baseline (2026-08-16):** See [`docs/audits/ECOSYSTEM_REBASELINE_PHASE0.md`](docs/audits/ECOSYSTEM_REBASELINE_PHASE0.md) for the full integration matrix, AI audit, and dependency maps (YASIN-DOCS #7).

> **Post Phase-0 certification:** See [`docs/audits/ECOSYSTEM_POST_PHASE0_CERTIFICATION.md`](docs/audits/ECOSYSTEM_POST_PHASE0_CERTIFICATION.md) (YASIN-DOCS #8).

## Core / Ecosystem Repositories

| Repository | Verified role | Default branch | Visibility | Current evidence |
|---|---|---:|---|---|
| `Yasin-core` | Shared runtime/foundation layer | `main` | Public | README + `yasin_core.version` **v3.3.0** |
| `Yasin-agent` | Independent agent planning/workflow/tools/sessions platform | `main` | Public | `agent_platform.__version__` **v1.0.0**; ADR-001; optional AI deferred #19 |
| `Yasin-AI` | **Canonical shared AI platform** | `main` | Public | `pyproject.toml` + README **v1.1.4** (contracts v1) |
| `YasinHub` | Lightweight status/health aggregation CLI (not full control plane) | `main` | Public | README (status store + process checker) |
| `YasinRelay` | Content relay pipeline: fetch → process → publish | `main` | Public | README **v2.0.0**; **Yasin-AI adapter merged** (#43); fetcher stabilized (#35); history secrets cleaned (#34) |
| `Yasinfeed` | Content collection, processing, and publishing engine | `main` | Public | README; **YasinAIProvider registered** (#52) |
| `Yasin-cli` | Cross-platform Node.js control/diagnostic CLI | `initial-setup` (main branch exists; set default via #34) | Public | README |
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
| `YasinPress-Rewrite-` | Production-oriented Python news collection, processing and publishing application | `main` | Public* | Verified runnable baseline; **1.0.0**; optional `AI_BACKEND=yasinai`; 114 tests pass |

\* Registry visibility may lag; treat code evidence as authoritative.

## Yasin-AI integration status (post Phase-0)

Primary content pipelines use **adapter-only** public contracts (`yasinai.contracts` / `yasinai.services`). No private Yasin-AI module imports.

| Consumer | Integration | Issue |
|----------|-------------|-------|
| YasinRelay | `yasinrelay.yasinai_adapter.YasinAIContentProcessor` (default `AI_PROVIDER=yasinai`, passthrough fallback) | #43 closed |
| Yasinfeed | `YasinAIProvider` registered in rewrite layer | #52 closed |
| YasinPress-Rewrite- | Optional `AI_BACKEND=yasinai` | path merged |
| Yasin-agent | Deferred | #19 |
| YasinHub | Not required (status surface) | — |
| Yasin-cli | Deferred | — |

See also: [`docs/audits/PIPELINE_OWNERSHIP.md`](docs/audits/PIPELINE_OWNERSHIP.md).

## YasinCoder — Current Architectural Record

YasinCoder is classified as the **canonical coding-agent repository**. The implementation and local/cloud provider integration work should converge there rather than being split across separate coding-agent repositories.

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

Detailed records remain under `docs/projects/yasincoder/`.

## Important Findings (current)

1. **Yasin-Core** is the foundation boundary (v3.3.0).
2. **Yasin-Agent** is an independent agent platform (not a Yasin-AI component); Core adapter present; AI optional/deferred.
3. **Yasin-AI v1.1.4** is the shared AI platform; consumers use only public contracts.
4. **YasinHub** is status-only CLI — do not describe as full control plane.
5. **YasinRelay** has canonical AI adapter, stabilized fetcher, and cleaned git history.
6. **YasinFeed** has Yasin-AI provider path registered.
7. **Yasin-cli** has a `main` branch; default remains `initial-setup` until maintainer flips settings (issue #34).
8. Pipeline overlap (Relay / Feed / Press) is **acceptable** as independent domain products sharing AI contracts only.

## Next Registry Upgrade

Maintain canonical repository URL, category, lifecycle, owner, dependencies, consumers, interfaces, stores, external integrations, evidence level, and cross-project impact. Detailed project records remain under `docs/projects/`.
