# YasinFeed — Public API & Application Contract v1

## Evidence

Source-audited against the current `yusi20006-max/YasinFeed` README and repository structure available to the GitHub integration.

**Evidence level:** S2/S3 for the module-level contract; exact symbol-level exports remain open because the expected model/module paths were not returned by the current source search.

## 1. Role

YasinFeed is the ecosystem's lightweight content aggregation, processing, and publishing application.

Its documented responsibilities are:

```text
Collect raw content
      ↓
Normalize / process / rewrite
      ↓
Persist articles
      ↓
Prepare outputs
      ↓
Publish to channels
```

The README explicitly excludes ecosystem orchestration, agent execution, and CLI ownership from YasinFeed. fileciteturn187file0

## 2. Application Modules

The documented module boundary is:

```text
yasinfeed/
├── api/
├── fetch/
├── models/
├── publisher/
├── rewrite/
├── scheduler/
├── storage/
├── config.py
├── logging.py
└── engine.py
```

### `api`

Query/delivery layer for PWA-compatible structured data and health endpoints.

### `fetch`

Remote feed/stream collection, RSS parsing, and inbound-content normalization.

### `models`

Shared application entities, including `Article` and `FeedSource` according to the documented architecture.

### `rewrite`

Content transformation boundary for summarization, translation, and rewriting. The README recommends adapter interfaces rather than embedding heavy AI frameworks in the core.

### `storage`

Persistence boundary. SQLite is explicitly supported; pluggable storage backends such as `SQLiteStorage` and `JSONStorage` are documented extension points.

### `scheduler`

Background job execution and lifecycle management. The documented default job is `fetch_and_process`.

### `publisher`

Destination adapters for Eitaa, PWA JSON, and RSS.

### `engine.py`

Central application lifecycle manager responsible for initialization/start/stop.

## 3. FEED-PUBLISHER Contract

### Contract ID

`FEED-PUBLISHER`

### Owner

YasinFeed

### Documented consumers/destinations

```text
Eitaa
PWA JSON
RSS
```

### Boundary

```text
Processed Article
      ↓
Publisher adapter
      ↓
Destination
```

The exact Python protocol/class signatures are **not yet source-verified** and must not be invented from module names.

Status: **Architecture/documentation verified; exact symbols open.**

## 4. Feed Fetch Contract

### Contract ID

`FEED-FETCH`

The fetch layer is responsible for:

- collecting raw feeds;
- parsing RSS;
- standardizing inbound items;
- isolating individual source failures;
- tracking source reliability;
- applying source priorities/weights;
- detecting duplicates and merging duplicate content.

This is an internal application boundary unless another ecosystem project explicitly consumes it.

Status: **Documented.**

## 5. Rewrite / AI Contract

### Contract ID

`FEED-REWRITE`

The rewrite layer provides the processing boundary for:

```text
summary
translation
rewriting
```

The README identifies LLM adapters such as Ollama/OpenAI/Claude as extension points and explicitly states that heavy AI models/frameworks should not be integrated directly into the core.

Therefore:

```text
YasinFeed → rewrite adapter
```

is supported by the architecture, while:

```text
YasinFeed → Yasin-AI
```

is **not automatically established** by the documentation.

Status: **Documented; cross-project AI contract unresolved.**

## 6. Storage Contract

### Contract ID

`FEED-STORAGE`

The application owns its persistence boundary and supports SQLite. JSON storage is documented as an extension point.

Storage should remain an implementation detail of YasinFeed unless a formal external data contract is created.

Important rule:

```text
YasinFeed storage
      ≠
Yasin ecosystem shared database
```

## 7. Scheduler Contract

### Contract ID

`FEED-SCHEDULER`

The scheduler is documented as a thread-safe background job layer with capabilities for:

```text
add job
remove job
pause job
resume job
track execution
record failures
```

The default pipeline job is:

```text
fetch_and_process
```

Conceptually:

```text
scheduler
   ↓
fetch
   ↓
storage
   ↓
rewrite
   ↓
publisher
```

This is **application-local orchestration**, not ecosystem-wide orchestration. YasinHub remains the ecosystem control/orchestration boundary.

## 8. API / Delivery Contract

YasinFeed exposes a documented API layer for:

```text
PWA-compatible structured data
health endpoints
```

Security foundations include:

```text
IP rate limiting
API keys / X-API-Key
session tokens
role-based permissions
security headers
```

Exact HTTP routes, request models, response schemas, status codes, and authentication middleware symbols remain open for source extraction.

## 9. Configuration Contract

Configuration precedence is source/documentation verified as:

```text
Defaults
   ↓
YAML config
   ↓
Environment variables
```

Supported environment overrides include:

```text
YASINFEED_ENV
YASINFEED_PORT
YASINFEED_HOST
YASINFEED_LOG_LEVEL
```

Nested configuration uses:

```text
YASINFEED__SECTION__KEY
```

Examples documented by the repository include publisher and fetch interval overrides.

## 10. Security Boundary

YasinFeed's API security belongs to the application itself.

It should not be confused with ecosystem-wide identity or authorization unless a formal Hub/Agent/CLI security contract is later introduced.

## 11. Ecosystem Boundary

Canonical relationship:

```text
                 YasinHub
                    │
              operational control
                    │
                    ▼
               YasinFeed
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      Fetch       Rewrite    Publisher
                                │
                         ┌──────┼──────┐
                         ▼      ▼      ▼
                       Eitaa   PWA    RSS
```

YasinFeed does **not** own:

```text
YasinHub orchestration
Yasin-Agent decision making
YasinCLI user interface
Yasin-Core runtime internals
```

These boundaries are explicitly documented in the repository README. fileciteturn187file0

## 12. Multi-Source Reliability

The application documents:

- source priority/weighting;
- dynamic reliability scoring;
- failure isolation;
- duplicate detection;
- duplicate merge strategies.

These features belong to the Feed aggregation domain and should remain inside Feed unless deliberately promoted to an ecosystem-wide service through an ADR.

## 13. Operational Requirements

The documented runtime target is Python `>=3.8` with minimal dependencies and compatibility with Linux/Termux environments.

The documented test command is:

```bash
python -m unittest discover -v
```

## 14. Contract Registry Update

Current state:

```text
FEED-PUBLISHER   → documentation verified
FEED-FETCH       → documentation verified
FEED-REWRITE     → documentation verified
FEED-STORAGE     → documentation verified
FEED-SCHEDULER   → documentation verified
FEED-API         → documentation verified
```

None of these should yet be represented as exact symbol-level APIs until the corresponding source files are individually inspected.

## 15. AI Agent Rules

When modifying YasinFeed:

1. Keep Feed focused on content collection, processing, and publishing.
2. Do not implement ecosystem orchestration inside Feed.
3. Do not turn Feed into an agent runtime.
4. Keep AI access behind rewrite/provider adapters.
5. Preserve source-failure isolation.
6. Keep application storage local to Feed unless a formal external contract is introduced.
7. Preserve the documented configuration precedence.
8. Update the contract registry when public API or provider boundaries change.
9. Use an ADR for new cross-project dependencies.

## 16. Open Source-Level Audit

The next exact extraction must locate and inspect:

```text
api/*
fetch/*
models/*
rewrite/*
storage/*
scheduler/*
publisher/*
engine.py
config.py
```

Priority is:

```text
models
publisher
rewrite
api
storage
scheduler
engine
```

The goal is to record exact classes, functions, signatures, schemas, errors, and public exports without guessing.

## Status

**YasinFeed Public API & Application Contract v1 — architecture/documentation baseline established; symbol-level source audit remains open.**
