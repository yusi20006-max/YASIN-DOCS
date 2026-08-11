# YasinFeed + YasinPress — Ecosystem Architecture

## YasinFeed

YasinFeed is the general-purpose content aggregation, processing, and publishing engine. Its explicit boundary excludes ecosystem orchestration, CLI management, and agent execution.

```text
Sources → Fetch → Normalize/Models → Rewrite/Summarize/Translate → Storage → Publisher
                                                                    ├─ RSS
                                                                    ├─ PWA JSON/API
                                                                    └─ Eitaa
```

Its scheduler can execute the default fetch → process → store → rewrite → publish cycle, making it an application pipeline rather than a passive library. The API boundary includes rate limiting, API keys/session tokens, role-based permissions, and security headers. Configuration follows defaults → YAML → environment overrides.

## YasinPress

YasinPress is a specialized Persian-news publishing engine optimized for Eitaa. It collects RSS sources, detects duplicates, rejects stale news, categorizes articles, optionally enriches them through an AI adapter, generates hashtags and daily digests, scores/prioritizes content, maintains a durable publication queue, rate-limits sending, and persists state in SQLite.

```text
RSS → Collection → Duplicate Detection → Age/Priority/Category → Optional AI → Builder/Formatter/Tags → Durable Queue → Rate Limiter → Publisher
```

### YasinPress v1.0.0 runtime verification

YasinPress v1.0.0 has been independently verified in a real Termux/Android environment, in addition to the repository CI environment.

Verified runtime:

- Android/Termux
- Python 3.14.6
- Editable installation via `python -m pip install -e .`
- Runtime dependencies installed successfully on ARM64 Android
- Pytest 9.1.1 installed successfully as a development/test dependency
- Full test suite: **114 passed**
- CLI import and execution: **passed**
- `yasinpress version`: **1.0.0**
- `yasinpress status`: **database: ok**
- `yasinpress health`: **database: ok**
- `yasinpress config`: **configuration: ok**

This confirms that YasinPress is not only CI-green but also operationally installable and executable in the intended Termux/Android environment.

## Relationship

| Project | Primary Role | Main Output |
|---|---|---|
| YasinFeed | General modular feed platform | RSS / PWA / Eitaa |
| YasinPress | Specialized Persian-news automation | Eitaa |
| YasinRelay | Telegram/content relay pipeline | Eitaa |

The projects overlap in content ingestion and publishing but have distinct application boundaries and should not be merged conceptually merely because their domains overlap.

## AI Boundary

YasinFeed provides rewrite/AI adapter extension points for providers such as Ollama, OpenAI, and Claude. YasinPress provides an optional AI adapter with a rule-based fallback. Neither repository should be documented as depending on Yasin-AI without source-level evidence.

## Operational Boundary

Both projects own their application pipelines and local state. YasinHub/YasinCLI should handle ecosystem lifecycle and operations rather than embedding their business logic.

```text
YasinCLI → YasinHub → {YasinFeed, YasinPress, YasinRelay}
                         │
                         ├─ Content Pipeline
                         ├─ News Pipeline
                         └─ Relay Pipeline
```

## Architectural Decisions / Risks

1. YasinFeed and YasinPress have overlapping RSS/news functionality. The ecosystem needs an explicit future decision on whether Press remains a specialized standalone product or becomes an application/profile built on shared Feed components.
2. AI provider ownership is distributed across application-specific adapters. A future shared AI contract or provider gateway may reduce duplication, but no dependency should be invented now.
3. Local SQLite databases are application state, not a shared ecosystem database.
4. Publishing adapters remain channel-specific and project-owned.

## Audit Status

- YasinFeed role: **CONFIRMED**
- YasinPress role: **CONFIRMED**
- YasinPress v1.0.0 Termux/Android runtime: **CONFIRMED**
- Feed/Press distinction: **CONFIRMED**
- Direct Feed → Yasin-AI dependency: **NOT ESTABLISHED**
- Direct Press → Yasin-AI dependency: **NOT ESTABLISHED**
- Hub/CLI operational boundary: **CONFIRMED**
- Shared content-platform opportunity: **IDENTIFIED, NOT YET ARCHITECTED**
