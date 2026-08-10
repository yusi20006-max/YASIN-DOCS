# YasinRelay — Project Knowledge Pack

## Identity
- Repository: `yusi20006-max/YasinRelay`
- Role: Telegram/content ingestion, transformation, deduplication, AI processing, media handling, and Eitaa publication pipeline.
- README states stable `v2.0.0`.

## Pipeline
```text
Telegram
 ↓
Collector
 ↓
Normalizer
 ↓
Validator
 ↓
Duplicate Detection / SQLite
 ↓
AIProcessor
 ↓
Media Processing
 ↓
Publisher
 ↓
Eitaa
```

## Owns
- Content pipeline orchestration
- Telegram fetcher integration
- Normalization/validation
- Deduplication
- AI processing boundary
- Media processing
- Publishing
- Scheduler
- Local pipeline state
- Structured logging

## AI Boundary
Relay exposes `AIProcessor` so provider implementations can change independently of the pipeline. Current architecture does not establish a direct dependency on Yasin-AI.

## Storage
SQLite stores operational pipeline state and duplicate/publication information. It is not ecosystem-wide memory.

## Scheduler / Execution
Supports single-run, scheduled execution, and a legacy loop mode according to the README. A Go-based fetcher is built under `fetcher/` and invoked as the Telegram collection frontend.

## Configuration
Environment variables include Eitaa credentials/channel, source channels, database path, logging level, schedule intervals, AI provider, AI API key/base URL/model.

## Testing
Python tests: `python3 -m pytest -v`. Go fetcher tests: `go test -v` under `fetcher/`.

## Boundary
Hub/CLI may control Relay operationally, but Relay owns its content-processing business logic.

## Change Rules
Changes to pipeline stage contracts, AIProcessor, publisher contracts, storage schema, fetcher protocol, or scheduler semantics require architecture/compatibility review.

## AI Agent Brief
For Telegram→Eitaa relay behavior, inspect Relay first. Keep AI behind the existing abstraction. Do not turn Relay's local events or SQLite into an implicit ecosystem-wide bus/database.
