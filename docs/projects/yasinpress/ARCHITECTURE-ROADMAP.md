# YasinPress — Architecture & Production Roadmap

> Status: **Architecture baseline defined; implementation is being brought into alignment.**
>
> This document is the planning authority for the YasinPress architecture. It deliberately separates the **verified/current implementation** from the **target production architecture** so that future AI agents and developers do not mistake planned components for already-shipped code.

## 1. Mission

YasinPress is the news-ingestion, intelligence, scheduling, and publishing engine of the Yasin ecosystem.

Its job is to:

1. discover and ingest news from multiple RSS sources;
2. normalize and validate articles;
3. determine freshness, duplicates, category, importance, and breaking status;
4. optionally enrich/rewrite content with AI;
5. maintain a persistent, fair, rate-limited publication queue;
6. publish to Eitaa and other supported publishers through adapters;
7. expose operational telemetry to a monitoring API and PWA;
8. emit hourly operational reports to a support channel;
9. recover from network, provider, source, and process failures without losing state.

YasinPress is a **publisher/processing service**, not the system-wide management layer. Higher-level management belongs to YasinHub/Yasin Agent and related ecosystem components.

## 2. Current Verified Baseline

The current YasinPress-Rewrite repository is a Python 3.13 production-oriented application with Clean Architecture boundaries. Its documented baseline includes:

- RSS ingestion and source management;
- article normalization/filtering/duplicate detection/validation/formatting;
- SQLite persistence, migrations, transactional unit-of-work and backups;
- scheduler and priority queue infrastructure;
- retry policy, cache, health checks, metrics, diagnostics and statistics;
- AI provider abstraction;
- publisher abstraction including Eitaa;
- configuration from defaults, JSON, YAML and environment variables;
- CLI, REST-style routing, plugin loading and security helpers.

These capabilities are **repository-backed baseline facts**. Individual production behaviors in the target specification below still require implementation and end-to-end verification.

## 3. Target Production Architecture

```text
                         ┌─────────────────────────┐
                         │       YasinPress        │
                         │   Application Runtime   │
                         └────────────┬────────────┘
                                      │
                 ┌────────────────────┼────────────────────┐
                 │                    │                    │
                 ▼                    ▼                    ▼
          Source Manager       Article Pipeline       Scheduler
                 │                    │                    │
          RSS / Adapters        Normalize             Scan jobs
                 │               Freshness              Reports
                 ▼               Dedup                   Watchdog
            Raw Articles        Intelligence               │
                                     │                      │
                                     ▼                      │
                              AI / Extraction              │
                                     │                      │
                                     └──────────┬───────────┘
                                                ▼
                                         Persistent Queue
                                                │
                                      Priority + Fairness
                                      Rate Limit + Retry
                                                │
                                                ▼
                                         Publisher Layer
                                                │
                              ┌─────────────────┼──────────────┐
                              ▼                 ▼              ▼
                           Eitaa            Webhook         Future
                                                │
                    ┌───────────────────────────┴────────────────────┐
                    ▼                                                ▼
             Monitoring Store                                  Event Stream
                    │                                                │
             ┌──────┴──────┐                                  ┌───────┴──────┐
             ▼             ▼                                  ▼              ▼
         Monitoring API   Hourly Reporter                     PWA       Support Channel
```

## 4. Architectural Layers

### 4.1 Source Layer

Responsibilities:

- RSS discovery and configuration;
- source adapters;
- fetch scheduling;
- timeout/retry handling;
- source health and response metrics;
- temporary degradation/disable/recovery;
- source priority and fairness metadata.

No source-specific parsing rule should leak into the core domain.

### 4.2 Article Intake & Normalization

Convert every source into a common article contract:

```text
Article
├── news_id
├── event_id (optional)
├── source_id
├── title
├── summary
├── content
├── canonical_url
├── published_at
├── received_at
├── author (optional)
├── image/media (optional)
├── category
├── priority
├── breaking
├── ai_status
└── status
```

All timestamps are normalized to a consistent timezone-aware representation.

### 4.3 Article Intelligence

Pipeline order:

```text
Normalize
  ↓
Validate
  ↓
Freshness
  ↓
Duplicate / Event matching
  ↓
Quality / Completeness
  ↓
Category
  ↓
Importance
  ↓
Breaking detection
  ↓
Media handling
  ↓
AI enrichment/rewrite
  ↓
Queue eligibility
```

### 4.4 Freshness Policy

Normal publication eligibility:

- article age **≤ 12 hours**;
- articles older than 12 hours are rejected from normal publication;
- a genuinely new update to an existing event is evaluated using the update publication timestamp;
- an old article is not republished merely because it is still relevant.

Breaking/freshness override is an explicit exception path and must be validated by the intelligence layer. It must not become a generic bypass for old news.

### 4.5 Deduplication and Event Continuity

YasinPress distinguishes:

```text
News ID   = unique identity of one article/version
Event ID  = identity of the underlying real-world event
```

The same article received repeatedly must never be published twice.

Different sources covering the same event may be grouped as one event while retaining source provenance.

A later article containing genuinely new information may be treated as a new article/update even when it belongs to the same event.

### 4.6 News ID

Target format:

```text
YP-YYMMDD-XXXXXX
```

Example:

```text
YP-260812-483721
```

The ID is generated once, persisted, and remains stable across restarts, queue retries, and monitoring views.

### 4.7 AI Layer

AI is an adapter-based capability, not a hard dependency of the core pipeline.

Target capabilities:

- rewrite/summarization;
- categorization;
- importance scoring;
- tagging;
- title optimization where appropriate.

If AI is unavailable, the pipeline must use a defined fallback path rather than blocking the entire service.

Every public AI-rewritten message is explicitly marked:

```text
🤖 بازنویسی با AI
```

The original source remains identifiable and linked.

### 4.8 Persistent Queue

The queue is durable and survives process/device restarts.

Required states:

```text
pending
processing
retrying
published
failed
```

Retry uses bounded exponential/backoff behavior. Permanently unsuccessful jobs enter a dead-letter state for inspection.

### 4.9 Fair Publishing

Global production target:

```text
Maximum: 10 published messages / hour
```

The scheduler must distribute capacity across active sources instead of allowing one high-volume feed to consume the entire hourly budget.

A source-specific cap may be configured; the global limit always wins.

Breaking articles receive higher priority but **cannot bypass the global hourly limit**.

### 4.10 Eitaa Message Format

Target public format:

```text
[optional 🔴 فوری] Title

Short rewritten/normalized summary.

━━━━━━━━━━━━━━

[optional 🤖 بازنویسی با AI] • 📰 Source Name
```

The **source name itself is the clickable link** to the original article. Raw URLs are not displayed.

The public channel should remain concise; internal News ID/Event ID values belong primarily in PWA/support diagnostics unless a later product decision requires public exposure.

### 4.11 Media Pipeline

Image handling is optional and fail-safe:

```text
RSS image
   ↓
validate
   ↓
source image fallback
   ↓
optimize
   ↓
publish
```

A media failure must never prevent a valid text-only article from being published.

### 4.12 Monitoring & Telemetry

Monitoring is a first-class subsystem with one shared data model for both PWA and support reports.

Tracked dimensions include:

- received;
- new;
- published;
- queued;
- duplicate;
- stale/old;
- failed;
- AI rewritten/fallback;
- source health;
- response time;
- Internet/network status;
- Eitaa status;
- scheduler/watchdog status;
- uptime and recovery events.

### 4.13 Hourly Support Report

Exactly one operational report is targeted for each hour: **24 reports per day**.

The report should include:

- received and published counts;
- processed/new/duplicate/stale counts;
- queue depth;
- number of active sources;
- per-source health and received counts;
- inactive/degraded sources;
- Internet/network availability;
- AI status;
- Eitaa status;
- scheduler/watchdog status;
- current hourly publishing usage.

Secrets and tokens must never appear in reports.

### 4.14 PWA Monitoring Dashboard

PWA is a read-first operational dashboard backed by the same monitoring data used for hourly reports.

Target views:

```text
Dashboard
Sources
Queue
Publishing
AI
System Health
Events
Reports
Settings (authenticated)
```

The dashboard must expose live operational state without exposing credentials.

Administrative actions such as restart, source modification, channel modification, or configuration changes require authentication and authorization.

### 4.15 Monitoring API

Target API surface:

```text
GET /api/status
GET /api/metrics
GET /api/sources
GET /api/queue
GET /api/publishing
GET /api/ai
GET /api/health
GET /api/events
```

The API is a read model over monitoring/state data. Secret values are never returned.

### 4.16 Scheduler

Target scheduled jobs:

```text
RSS scan             every ~5 minutes
Hourly report        every hour
Watchdog             short fixed interval
Queue processing     continuous/scheduled
Health checks        periodic
```

Intervals must be configurable rather than hard-coded.

### 4.17 Watchdog & Recovery

Watchdog monitors:

- process/runtime health;
- Internet availability;
- RSS source health;
- AI provider health;
- Eitaa availability;
- scheduler liveness;
- queue progress.

Recovery policy:

```text
Detect → Retry → Recover → Resume → Report
```

Recovery must preserve persistent queue and deduplication state.

## 5. Configuration Model

Configuration is centralized and layered:

```text
Environment / Secrets
        ↓
User configuration
        ↓
Safe defaults
```

Target configuration domains:

- Eitaa;
- RSS sources;
- AI providers;
- freshness;
- publishing limits;
- queue/retry;
- scheduler;
- monitoring;
- PWA;
- watchdog.

Credentials such as Eitaa tokens and AI keys are never committed to source control, database exports, logs, PWA responses, or support reports.

## 6. Persistence Model

SQLite remains the default local production state store for the Termux deployment target.

Core state domains:

```text
articles
publish_queue
rss_sources
metrics
events
publish_attempts
system_health
```

Schema design must support transactional updates so that publication, deduplication, and queue state cannot become inconsistent after a crash.

## 7. CLI / Operations

Target operational interface:

```text
yasinpress start
yasinpress stop
yasinpress restart
yasinpress status
yasinpress logs
yasinpress doctor
yasinpress run
```

Startup must produce a concise operational confirmation such as:

```text
YasinPress is active
```

The terminal should show health/statistics rather than dumping every received article. Useful periodic output includes source counts and hourly publication statistics.

## 8. Production Lifecycle

```text
Configure
   ↓
Validate
   ↓
Start
   ↓
Fetch
   ↓
Intelligence
   ↓
Queue
   ↓
Publish
   ↓
Monitor
   ↓
Recover when needed
   ↓
Hourly report
```

## 9. Implementation Roadmap

### Phase 0 — Architecture Lock
- [x] Define system boundaries.
- [x] Define target pipeline.
- [x] Define freshness policy (12h).
- [x] Define global publication limit (10/hour).
- [x] Define source fairness requirement.
- [x] Define News ID/Event ID distinction.
- [x] Define AI transparency marker.
- [x] Define linked source-name output.
- [x] Define hourly support reporting.
- [x] Define PWA/Monitoring direction.

### Phase 1 — Core & Persistence
- [ ] Verify current domain models against this contract.
- [ ] Finalize Article model and status transitions.
- [ ] Finalize News ID generation/persistence.
- [ ] Finalize Event ID/grouping model.
- [ ] Finalize SQLite schema and migrations.
- [ ] Finalize persistent queue state transitions.
- [ ] Add crash/restart recovery tests.

### Phase 2 — Source & RSS
- [ ] Finalize Source Adapter contract.
- [ ] Implement/verify generic RSS adapter.
- [ ] Implement/verify source-specific adapters where justified.
- [ ] Add source health tracking.
- [ ] Add discovery/default-feed handling.
- [ ] Add source degradation and automatic recovery.
- [ ] Verify all configured feeds independently.

### Phase 3 — Article Intelligence
- [ ] Normalize timestamps/timezones.
- [ ] Enforce ≤12h freshness for normal articles.
- [ ] Implement breaking exception path.
- [ ] Implement exact/cross-source deduplication.
- [ ] Implement event continuity/update detection.
- [ ] Implement quality/completeness scoring.
- [ ] Implement category and importance scoring.

### Phase 4 — AI
- [ ] Verify provider abstraction.
- [ ] Implement rewrite/summarization contract.
- [ ] Implement AI fallback.
- [ ] Persist AI processing status.
- [ ] Add transparent AI marker to public output.
- [ ] Add AI metrics to monitoring.

### Phase 5 — Queue & Publishing
- [ ] Implement/verify priority queue.
- [ ] Implement global 10/hour limiter.
- [ ] Implement fair scheduling across sources.
- [ ] Implement retry/backoff/dead-letter handling.
- [ ] Implement Eitaa adapter.
- [ ] Finalize public message format.
- [ ] Make source name the article link.
- [ ] Verify text-only fallback when media fails.

### Phase 6 — Monitoring
- [ ] Define unified telemetry/event schema.
- [ ] Implement operational metrics store.
- [ ] Implement hourly report generator.
- [ ] Implement support-channel publisher.
- [ ] Add health/network/provider diagnostics.
- [ ] Ensure exactly one hourly report target per hour.

### Phase 7 — Monitoring API & PWA
- [ ] Implement read-only monitoring API.
- [ ] Implement PWA dashboard.
- [ ] Add source/queue/publishing/system-health views.
- [ ] Add historical reports/metrics.
- [ ] Add authenticated administrative actions only after read-only dashboard is stable.

### Phase 8 — Scheduler, Watchdog & Termux Operations
- [ ] Verify scheduler lifecycle.
- [ ] Add watchdog liveness checks.
- [ ] Add provider/source recovery.
- [ ] Add process restart/recovery.
- [ ] Add persistent queue recovery.
- [ ] Add Termux auto-start/runbook.
- [ ] Verify clean `start/status/stop/restart` lifecycle.

### Phase 9 — End-to-End Production Validation
- [ ] Multi-source ingestion test.
- [ ] Duplicate test.
- [ ] 12-hour freshness test.
- [ ] Breaking-news test.
- [ ] AI failure/fallback test.
- [ ] Eitaa failure/retry test.
- [ ] 10/hour rate-limit test.
- [ ] Fair-source distribution test.
- [ ] Crash/restart queue recovery test.
- [ ] Hourly report test.
- [ ] PWA consistency test.
- [ ] 24-hour soak test.

### Phase 10 — Release Freeze
- [ ] Production configuration freeze.
- [ ] Security/secret audit.
- [ ] Test suite green.
- [ ] Documentation synchronized.
- [ ] Version/tag/release created.
- [ ] Termux production runbook verified.

## 10. Multi-AI Development Model

AI tools may collaborate, but they must not independently redefine the architecture.

### Primary architecture authority

The YasinPress architecture in this document is the shared contract. Any proposed deviation must be documented and reviewed before implementation.

### Builder

Jules/Coding agents may implement scoped GitHub Issues on isolated branches, with tests and a PR.

### Reviewers

Other AI systems may perform independent:

- code review;
- edge-case analysis;
- architecture review;
- test design;
- security review;
- PWA/UX review.

### Merge rule

```text
Issue
 ↓
Isolated branch
 ↓
Implementation
 ↓
Tests
 ↓
Independent review
 ↓
PR
 ↓
Merge
```

No AI should make unreviewed architectural changes directly on production/main.

## 11. Non-Goals / Guardrails

YasinPress must not:

- expose secrets through logs, reports, or APIs;
- bypass the global publication limit during recovery;
- republish old news merely because it remains relevant;
- allow one source to monopolize the publication budget;
- treat AI availability as a single point of failure;
- let a broken RSS source stop the entire pipeline;
- copy source articles wholesale as the public output;
- make PWA administrative controls unauthenticated.

## 12. Definition of Done

YasinPress is considered production-ready when:

1. all Phase 1–9 acceptance tests pass;
2. persistent state survives process/device restart;
3. normal news older than 12 hours is rejected;
4. breaking exceptions are explicitly validated;
5. no duplicate article is published twice;
6. global publication stays within 10/hour;
7. active sources receive fair publication opportunities;
8. AI failure does not stop valid publishing;
9. Eitaa/network failures recover without data loss;
10. PWA and hourly support reports use the same telemetry source;
11. watchdog and scheduler recover safely;
12. secrets are absent from logs/API/reports;
13. the 24-hour soak test passes;
14. YasinDocs and repository documentation agree with the verified implementation.

## 13. Source of Truth Rule

- **YasinPress repository** = implementation truth.
- **This document** = target architecture and delivery roadmap.
- **YasinDocs** = cross-project documentation and handoff truth.
- **ADRs** = authoritative record for decisions that intentionally change this architecture.

When implementation and this roadmap disagree, do not silently assume either is correct: record the discrepancy, verify the repository, and update the appropriate document/ADR.
