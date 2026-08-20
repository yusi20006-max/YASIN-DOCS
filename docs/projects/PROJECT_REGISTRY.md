# Yasin Project Registry

This is the human-readable companion to `PROJECT_REGISTRY.yaml`.

## Core / Primary Ecosystem

| Project | Repository | Category | Current documented role | Confidence |
|---|---|---|---|---|
| Yasin-Core | `yusi20006-max/Yasin-core` | Foundation | Core runtime/foundation | Partial |
| Yasin-Agent | `yusi20006-max/Yasin-agent` | Agent | Agent platform/runtime | Partial |
| Yasin-AI | `yusi20006-max/Yasin-AI` | AI | AI ecosystem component | Partial |
| YasinHub | `yusi20006-max/YasinHub` | Management | Management/status component | Partial |
| YasinRelay | `yusi20006-max/YasinRelay` | Integration | Relay/integration layer | Partial |
| YasinFeed | `yusi20006-max/Yasinfeed` | Application | Content generation/publishing pipeline | Partial |
| YasinPress | `yusi20006-max/Yasinpress` | Application | Persian news collection/publishing | Partial |
| YasinCLI | `yusi20006-max/Yasin-cli` | Control Plane | Unified ecosystem CLI | Partial |
| YASIN-DOCS | `yusi20006-max/YASIN-DOCS` | Documentation | Ecosystem source of truth | Verified |

## Operations / Optional Layer

| Project | Repository | Category | Current documented role | Confidence | Dependency status |
|---|---|---|---|---|---|
| Yasin-Operations | `yusi20006-max/Yasin-Operations` | Operations | Modular Operations Agent: operations, diagnostics, health checks, service lifecycle management, runtime inspection, operational tooling, optional adapters/integrations | Provisional | Independent — optional, no mandatory cross-repository dependency in either direction |

Yasin-Operations is a newly registered, independent project (registered 2026-08-17, Issue #27). It does not own Core AI capabilities (owned by Yasin-AI), publishing/news-processing domain (owned by YasinPress), or relay/feed transport responsibilities (owned by YasinRelay). Its absence must not break Yasin-AI, YasinPress, YasinRelay, or Hermes. See `docs/adr/ADR-0012-yasin-operations-boundary.md` for the full boundary decision and `docs/audits/ACTIVITY_LOG_2026-08-17.md` for verification evidence.

## Related / Supporting Projects

| Project | Repository | Category | Documented role |
|---|---|---|---|
| OpenFeed | `yusi20006-max/Openfeed` | Integration | Stable Telegram public-channel fetcher/API/PWA |
| FeedBridge | `yusi20006-max/Feedbridge` | Application | Telegram content bridge and Eitaa publisher |
| TJC | `yusi20006-max/TJC` | Developer tooling | Jules automation CLI for Termux/POSIX shell |
| Termux Backup Manager | `yusi20006-max/Termux-BackupManager` | Tooling | Termux backup/restore/migration |

## Confidence Model

- **Verified:** directly supported by repository evidence.
- **Partial:** repository exists and role has evidence, but architecture is not fully audited.
- **Provisional:** working hypothesis requiring source-level verification.
- **Unknown:** insufficient evidence.

## Important Architectural Rule

The registry deliberately leaves `depends_on` and `consumers` empty until source-level evidence establishes them. This prevents the central architecture document from turning assumptions into false dependencies.

## Next Audit Target

Phase 5 will populate detailed project records and promote relationships from partial/provisional to verified as evidence is collected.
