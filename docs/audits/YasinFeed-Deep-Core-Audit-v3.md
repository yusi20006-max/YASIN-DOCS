# YasinFeed — Deep Core Audit v3

- Repository: `yusi20006-max/Yasinfeed`
- Audited release: `v1.0.0`
- Audit date: 2026-08-11
- Status: **Deep source/PR evidence recorded**

## 1. Release Evidence

Merged PR #51 finalized YasinFeed as `1.0.0`. The release PR reports 128 tests passing and describes the production boundary as a lightweight Python backend for feed collection, processing, rewriting and outbound distribution.

The release documentation explicitly states that YasinHub orchestration and Yasin-Agent workflow execution are outside YasinFeed's responsibility.

## 2. Fetch Layer

The FetchModule is a genuine aggregation layer rather than a single-feed wrapper.

### Flow

```text
Storage: enabled FeedSources
        ↓
FetchModule
        ↓
FeedFetcher
        ↓
retry / exponential backoff
        ↓
raw normalized items
        ↓
duplicate grouping
        ↓
priority / weight / reliability selection
        ↓
final feed items
```

### Source reliability

Each source tracks:

- `fetch_count`
- `success_count`
- `failure_count`
- `reliability_score`
- `last_error`
- `last_fetched_at`

A source failure is isolated so other enabled sources can still produce output.

### Duplicate handling

Items are grouped using the article identifier/URL and normalized title. The configured merge strategy is `priority` by default, with a `combine` mode that preserves unique alternative source content.

Source ranking considers:

```text
priority
weight
reliability_score
```

This is a strong standalone feed-ingestion boundary.

## 3. Retry Semantics

The retry helper implements exponential backoff:

```text
attempt 1 → delay
attempt 2 → delay × backoff
attempt 3 → delay × backoff²
```

The FetchModule currently invokes it with three retries, one-second initial delay, and backoff factor two.

This provides network-failure tolerance without requiring an external orchestration service.

## 4. Rewrite / Content Pipeline

`ContentPipeline` is a sequential stage engine. The release architecture identifies these default stages:

1. `SanitizationStage`
2. `RewriteStage`
3. `TranslationStage`
4. `ContentAnalysisStage`
5. `MetadataTaggingStage`

The pipeline records execution metadata on each Article, including:

- stages executed;
- failures;
- critical/non-critical status;
- total duration;
- completion timestamp.

### Failure model

Each stage has a `critical` flag.

Critical failure:

```text
stage fails
  ↓
article.rewrite_status = failed
  ↓
pipeline aborts
  ↓
error propagates
```

Non-critical failure:

```text
stage fails
  ↓
record failure
  ↓
run fallback()
  ↓
continue pipeline
```

This is an explicit resilience contract and is appropriate for a content-processing service.

## 5. Content Intelligence

`ContentIntelligenceEngine` is provider-agnostic and pure Python. It does not itself rewrite the article.

It generates:

- language detection;
- lexicon sentiment score/label;
- readability statistics;
- topic/keyword frequency;
- urgency/priority score;
- relevance score;
- dispatch recommendation;
- confidence;
- matched urgency triggers.

The output is stored under `article.pipeline_metadata["intelligence"]`.

### Architectural consequence

YasinFeed can produce structured intelligence signals without requiring Yasin-Agent. Yasin-Agent can consume these signals later through an integration boundary, but the feed-processing engine remains independently functional.

## 6. Storage

The repository has a storage abstraction with SQLite and JSON-backed implementations.

The SQLite implementation supports backward-compatible column additions for feed-source reliability/priority metadata and user roles.

The storage module wraps backend operations with monitoring instrumentation such as:

```text
db_save_feed_source
db_get_feed_source
db_list_feed_sources
db_save_article
db_get_article
db_list_articles
```

This confirms storage is an internal subsystem with a backend abstraction rather than a shared ecosystem database requirement.

## 7. Observability

The monitoring layer provides a thread-safe `Metrics` registry and structured JSON Lines event logging.

Tracked areas include:

- fetch cycles;
- fetched articles;
- processed articles;
- database queries;
- pipeline stage timing;
- total errors;
- per-component error counters.

The health/status API exposes metrics and recent error snapshots.

This makes YasinFeed operationally diagnosable without requiring YasinHub.

## 8. API and Security

The REST layer is based on Python's standard-library `ThreadingHTTPServer`.

Observed API capabilities include:

- health endpoints;
- article endpoints;
- source endpoints;
- scheduler endpoint;
- statistics endpoint;
- registration/login endpoints;
- Bearer session authentication;
- API-key authentication;
- role-based permissions;
- rolling IP rate limiting;
- security headers;
- JSON request validation;
- structured error responses.

The default API security configuration is disabled until explicitly enabled. Production documentation separately recommends secure localhost binding unless an external security boundary is deliberately configured.

## 9. Integration Boundary — Important Architectural Finding

PR #50 introduced an `IntegrationModule` with:

- `BaseIntegrationProvider`
- `HubIntegrationProvider`
- `AgentIntegrationProvider`
- event hooks;
- dynamic plugin loading.

This does **not** make YasinFeed dependent on YasinHub or Yasin-Agent.

Instead, it creates a provider interface for future communication.

The distinction is important:

```text
YasinFeed owns processing.

IntegrationModule exposes extension points.

Hub/Agent providers are adapters.

YasinHub and Yasin-Agent remain external services.
```

## 10. Plugin Loader

`PluginLoader` dynamically discovers Python provider classes and optional `register_plugin()` hooks using standard-library `importlib` and reflection.

This enables extensions without modifying the core engine.

However, plugins are executable Python and therefore must be treated as trusted code. The loader is an extension mechanism, not a sandbox.

## 11. Release-Readiness Assessment

| Area | Assessment |
|---|---|
| Standalone runtime | Strong |
| Fetch aggregation | Strong |
| Retry/failure isolation | Strong |
| Duplicate/merge handling | Strong |
| Content pipeline | Strong |
| Content intelligence | Strong |
| Storage abstraction | Strong |
| Observability | Strong |
| API/security foundation | Strong, but standard-library HTTP bound |
| Hub/Agent integration | Adapter-ready, not dependency-bound |
| Plugin mechanism | Functional, trusted-code model |
| Termux compatibility | Declared and designed |
| Current independent runtime verification | Still requires live validation |

## 12. Final Architectural Decision

YasinFeed is sufficiently self-contained to remain a fully independent product.

The ecosystem should preserve this model:

```text
                    ┌─────────────────┐
                    │    YasinFeed    │
                    │ fetch/process/  │
                    │ rewrite/store/  │
                    │ publish         │
                    └────────┬────────┘
                             │
                   public API / adapters
                             │
             ┌───────────────┴───────────────┐
             ▼                               ▼
        YasinHub                         Yasin-Agent
     orchestration                    agent workflows
```

Neither external service is required for YasinFeed's own core runtime.

## 13. Next Audit Target

The next pass should focus specifically on **Publisher + API runtime + real Termux execution**, including the actual RSS/PWA/Eitaa publishing paths, scheduler-to-publisher flow, and whether a clean install can ingest a real RSS source and produce/persist/publish an article without ecosystem dependencies.
