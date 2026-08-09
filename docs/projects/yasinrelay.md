# YasinRelay — Project Architecture Record

## Identity

- Repository: `yusi20006-max/YasinRelay`
- Documented version: `2.0.0 stable`
- Role: Telegram-to-Eitaa content relay pipeline

## Pipeline

```text
Telegram channels
  -> CollectorStage (Go CLI subprocess)
  -> NormalizerStage
  -> ValidatorStage
  -> DuplicateStage (SQLite)
  -> AIProcessorStage
  -> MediaPrepStage
  -> PublisherStage (Eitaa)
```

## Core Components

- SQLite storage/models
- modular pipeline engine
- AI processor interface
- media processor
- structured logging
- native scheduler
- compatibility pipeline wrapper
- CLI
- Go-based Telegram fetcher

## Runtime Modes

- single run
- recommended scheduled run
- legacy loop mode

## Configuration

Documented environment variables include Eitaa credentials/destination, source channels, SQLite path, log level, scheduling, AI provider, API key/base URL/model.

## Integration Boundary

The repository documents a Go fetcher derived around the OpenFeed-style fetching architecture and a Python pipeline around it. The exact current code relationship with the separate OpenFeed repository must be verified before declaring a direct package dependency.

## Agent-related Features

The README also documents lifecycle hooks, an in-process event bus and agent configuration. These should be treated as YasinRelay-local capabilities unless source audit proves they are shared imports from Yasin-Agent/Core.

## Testing

Python tests use pytest; Go fetcher tests use `go test`.

## Audit Status

**Level 3:** pipeline architecture and runtime/configuration boundaries are well documented. Exact OpenFeed dependency, Yasin-Core/Agent contracts, API surface and deployment topology require source audit.
