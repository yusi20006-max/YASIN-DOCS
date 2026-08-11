# YasinFeed + YasinPress — Ecosystem Architecture

## YasinFeed

YasinFeed is the general-purpose content aggregation, processing, storage, and publishing engine. It is a **standalone application runtime** and does not require YasinPress, YasinRelay, YasinHub internals, YasinCLI internals, or Yasin-AI in order to execute its core pipeline.

```text
Sources → Fetch → Normalize/Models → Rewrite/Summarize/Translate → Storage → Publisher
                                                                    ├─ RSS
                                                                    ├─ PWA JSON/API
                                                                    └─ Eitaa
```

Its scheduler can execute the default fetch → process → store → rewrite → publish cycle, making it an application pipeline rather than a passive library. The API boundary includes rate limiting, API keys/session tokens, role-based permissions, and security headers. Configuration follows defaults → YAML → environment overrides.

## YasinPress

YasinPress is a specialized Persian-news publishing engine optimized for Eitaa. It is a **standalone application runtime** and does not require YasinFeed, YasinRelay, YasinHub internals, YasinCLI internals, or Yasin-AI in order to execute its core pipeline.

It collects RSS sources, detects duplicates, rejects stale news, categorizes articles, optionally enriches them through an AI adapter, generates hashtags and daily digests, scores/prioritizes content, maintains a durable publication queue, rate-limits sending, and persists state in SQLite.

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

## Independence Decision

YasinFeed and YasinPress are intentionally maintained as two separate products. **Neither is a runtime dependency of the other.**

Each must be capable of:

- independent installation;
- independent configuration;
- independent startup and shutdown;
- independent state management;
- independent testing and release;
- independent publishing operation.

The applications may share architectural ideas or future reusable contracts, but conceptual overlap does not create a runtime dependency.

```text
                    YasinHub / YasinCLI
                     operational control
                       /           \
                      ▼             ▼
                 YasinFeed     YasinPress
                  standalone      standalone
                  runtime         runtime
```

Operational control from Hub/CLI is an ecosystem concern. It must not require Feed or Press to import Hub internals.

## Relationship

| Project | Primary Role | Standalone Output |
|---|---|---|
| YasinFeed | General modular feed platform | RSS / PWA / Eitaa |
| YasinPress | Specialized Persian-news automation | Eitaa |
| YasinRelay | Telegram/content relay pipeline | Eitaa |

The projects overlap in content ingestion and publishing but have distinct application boundaries. YasinFeed must not be used merely as an implicit base runtime for YasinPress, and YasinPress must not become a hidden dependency of YasinFeed.

## AI Boundary

YasinFeed provides rewrite/AI adapter extension points for providers such as Ollama, OpenAI, and Claude. YasinPress provides an optional AI adapter with a rule-based fallback. Neither repository should be documented as depending on Yasin-AI without source-level evidence.

## Operational Boundary

Both projects own their application pipelines and local state. YasinHub/YasinCLI may control them through public operational boundaries, but their core execution remains independent.

```text
YasinCLI → YasinHub → {YasinFeed, YasinPress, YasinRelay}
                         │
                         ├─ Feed lifecycle/status
                         ├─ Press lifecycle/status
                         └─ Relay lifecycle/status
```

## Storage Boundary

Feed and Press own separate application state. There is no confirmed shared application database.

```text
YasinFeed  → Feed-owned application storage
YasinPress → Press-owned SQLite application state
```

A shared datastore requires an explicit ADR and contract and must not be introduced through accidental coupling.

## Architectural Decisions / Risks

1. YasinFeed and YasinPress intentionally remain standalone products. This decision is recorded in **ADR-001**.
2. Some RSS, processing, configuration, and publishing logic may be duplicated. Future reuse should happen through deliberate shared libraries or contracts rather than application-to-application runtime dependency.
3. AI provider ownership is distributed across application-specific adapters. A future shared AI contract or provider gateway may reduce duplication, but no dependency should be invented now.
4. Local SQLite/datastore state is application state, not shared ecosystem memory.
5. Publishing adapters remain channel-specific and project-owned.

## Audit Status

- YasinFeed role: **CONFIRMED**
- YasinPress role: **CONFIRMED**
- YasinPress v1.0.0 Termux/Android runtime: **CONFIRMED**
- Feed/Press distinction: **CONFIRMED**
- Feed standalone runtime: **CONFIRMED BY ARCHITECTURE DECISION**
- Press standalone runtime: **CONFIRMED BY ARCHITECTURE DECISION**
- Feed → Press runtime dependency: **PROHIBITED / NOT REQUIRED**
- Press → Feed runtime dependency: **PROHIBITED / NOT REQUIRED**
- Direct Feed → Yasin-AI dependency: **NOT ESTABLISHED**
- Direct Press → Yasin-AI dependency: **NOT ESTABLISHED**
- Hub/CLI operational boundary: **CONFIRMED**
- Shared content-platform opportunity: **IDENTIFIED, NOT YET ARCHITECTED**
