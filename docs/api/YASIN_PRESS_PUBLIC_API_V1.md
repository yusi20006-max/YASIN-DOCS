# YasinPress — Public API & Application Contract v1

## Evidence

Source/documentation-verified against `yusi20006-max/Yasinpress` README.

Repository version identified by README: **2.0.0**.

The current README provides a detailed module-level architecture, but the available source search did not return reliable symbol-level matches for the expected modules. Therefore this document deliberately separates documented application boundaries from exact source-verified Python symbols.

## 1. Role

YasinPress is a Persian news collection and publishing engine designed to collect news from multiple RSS sources, process and prioritize articles, and publish them to Eitaa.

Its AI layer is optional and currently documented as **Cloudflare Workers AI**.

Core responsibilities include:

```text
RSS collection
    ↓
Deduplication
    ↓
Age filtering
    ↓
Categorization
    ↓
Optional AI processing
    ↓
News formatting
    ↓
Prioritization
    ↓
Persistent publish queue
    ↓
Rate-limited Eitaa publishing
```

The README explicitly states that the application falls back to rule-based processing when AI is unavailable. fileciteturn188file0

## 2. Application Modules

The documented module surface is:

```text
run.py
config.py
pipeline.py
fetch_news.py
rss_engine.py
duplicate_engine.py
duplicate_detector.py
similarity.py
category_engine.py
ai_engine.py
daily_digest.py
news_builder.py
message_builder.py
formatter.py
tag_engine.py
post_counter.py
source_names.py
logo_manager.py
send_queue.py
queue_manager.py
rate_limiter.py
eitaa_sender.py
media_sender.py
publish_engine.py
main_controller.py
process_lock.py
database.py
logger.py
```

These names establish the documented module responsibilities; they should not automatically be treated as stable public Python APIs.

## 3. RSS Collection Contract

### Contract ID

`PRESS-RSS-COLLECTOR`

### Responsibility

Collect news concurrently from configured news-agency RSS feeds.

### Configuration boundary

```text
sources.json
```

The collector must produce normalized article/news records for the downstream pipeline.

### Status

**Documented application contract.** Exact class/function signatures remain source-audit work.

## 4. Deduplication Contract

### Contract ID

`PRESS-DEDUPE`

The README documents duplicate detection using:

```text
rapidfuzz + database
```

and an explicit similarity/deduplication module family.

The system also prevents publishing news older than 24 hours.

### Architectural rule

Deduplication is application-local to YasinPress unless a future ecosystem-level content identity service is explicitly introduced.

## 5. Categorization Contract

### Contract ID

`PRESS-CATEGORY`

Documented categories include:

```text
اقتصاد
بین‌الملل
ورزش
سلامت
فناوری
فرهنگ
آموزش
```

The architecture supports a rule-based category engine and an optional AI-assisted categorization path.

## 6. AI Processing Contract

### Contract ID

`PRESS-AI`

### Provider

Cloudflare Workers AI.

### Optional capabilities

```text
headline rewriting
natural summarization
smart categorization
automatic hashtags
breaking-news detection
daily digest generation
```

### Failure behavior

AI is explicitly optional. When AI credentials/service are unavailable, the application falls back to rule-based processing instead of requiring AI for basic operation. fileciteturn188file0

### Architectural consequence

This confirms:

```text
YasinPress → Cloudflare Workers AI
```

as a documented provider integration.

It does **not** confirm:

```text
YasinPress → Yasin-AI
```

No such cross-project dependency should be added to the canonical architecture without an explicit adapter/contract.

## 7. News Formatting Contract

### Contract ID

`PRESS-NEWS-BUILDER`

The documented formatter family contains:

```text
news_builder
message_builder
formatter
tag_engine
source_names
logo_manager
post_counter
```

Their combined responsibility is to turn normalized/processed news into a publishable Eitaa message and associated media/metadata.

Exact schemas remain open.

## 8. Persistent Publishing Queue

### Contract ID

`PRESS-PUBLISH-QUEUE`

The documented queue family contains:

```text
send_queue
queue_manager
rate_limiter
```

The README explicitly describes the publish queue as persistent/on-disk and resilient to interruptions.

This gives YasinPress an important reliability boundary:

```text
News pipeline
    ↓
Persistent queue
    ↓
Rate limiter
    ↓
Eitaa sender
```

## 9. Eitaa Publishing Contract

### Contract ID

`PRESS-EITAA-PUBLISHER`

Documented modules:

```text
eitaa_sender
media_sender
publish_engine
```

The publisher is responsible for communicating with Eitaayar and enforcing application-level publishing constraints.

The README documents known Eitaayar limitations including unsupported `parse_mode` and `reply_markup` behavior.

Therefore message formatting must remain compatible with plain-text publishing. fileciteturn188file0

## 10. Storage Contract

### Contract ID

`PRESS-STORAGE`

YasinPress uses SQLite for persistent application data.

The documented storage owner is:

```text
database.py
```

The storage must be treated as YasinPress-owned application state, not as ecosystem-wide shared memory.

## 11. Process Safety

### Contract ID

`PRESS-PROCESS-LOCK`

`process_lock.py` provides the documented mechanism for preventing multiple simultaneous instances.

This is an application-local operational invariant.

## 12. Runtime Environment

The application is explicitly designed for:

```text
Termux / Android
Python 3.10+
```

and can run as:

```text
python run.py
```

The project therefore remains compatible with the broader Yasin ecosystem's Termux-oriented operational environment. fileciteturn188file0

## 13. Architectural Boundary

```text
RSS Providers
     ↓
YasinPress Collection
     ↓
Processing / Deduplication / Categorization
     ↓
Optional Cloudflare Workers AI
     ↓
Formatting / Prioritization
     ↓
Persistent Queue
     ↓
Rate Limiter
     ↓
Eitaa Publisher
```

YasinPress owns the news-publishing application pipeline.

It should not absorb:

```text
Yasin-Core runtime responsibilities
Yasin-Agent orchestration
YasinHub control-plane responsibilities
YasinRelay's Telegram→Eitaa relay pipeline
Yasin-AI's platform responsibilities
```

## 14. Contract Status Update

`PRESS-RSS-COLLECTOR`

**Documented / architecture verified.**

`PRESS-DEDUPE`

**Documented / architecture verified.**

`PRESS-AI`

**Provider integration documented.**

`PRESS-PUBLISH-QUEUE`

**Documented / architecture verified.**

`PRESS-EITAA-PUBLISHER`

**Documented / architecture verified.**

`PRESS-STORAGE`

**Documented / architecture verified.**

Exact public symbols and signatures remain **open** because the available GitHub source search did not provide reliable symbol-level evidence in this audit pass.

## 15. AI Agent Rules

When modifying YasinPress:

1. Preserve the fallback-to-rule-based behavior unless deliberately changing reliability semantics.
2. Treat Cloudflare AI as an optional provider, not as ecosystem-wide AI ownership.
3. Keep the persistent queue durable across process interruptions.
4. Preserve rate limiting around Eitaa publishing.
5. Keep SQLite state local to YasinPress unless a deliberate architecture change is approved.
6. Do not introduce a direct dependency on Yasin-AI without an explicit integration contract and ADR.
7. Respect documented Eitaayar API limitations.
8. Update this contract document when module responsibilities or public integration boundaries change.
9. Update the ecosystem Contract Registry for cross-project changes.

## 16. Open Work

For full source-level API completion, inspect:

```text
pipeline.py
rss_engine.py
ai_engine.py
database.py
publish_engine.py
eitaa_sender.py
send_queue.py
queue_manager.py
rate_limiter.py
config.py
run.py
```

Extract exact:

- classes;
- functions;
- signatures;
- models;
- return schemas;
- exceptions;
- retry behavior;
- queue state transitions;
- provider request/response schemas.

## Status

**YasinPress Public API & Application Contract v1 — documented architecture baseline complete; symbol-level source audit remains open.**
