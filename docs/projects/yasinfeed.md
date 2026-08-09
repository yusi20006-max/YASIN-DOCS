# YasinFeed — Project Architecture Record

## Identity

- Repository: `yusi20006-max/Yasinfeed`
- Role: lightweight modular content collection, processing and publishing engine

## Responsibility

YasinFeed explicitly limits itself to content collection, processing and publishing pipes/stubs. It does not own ecosystem orchestration, agent decision-making/workflows, or the ecosystem-wide CLI.

## Module Map

```text
api/         PWA/integration and health endpoints
fetch/       feed collection/parsing/normalization
models/      Article/FeedSource and shared schemas
publisher/   Eitaa/PWA/RSS output adapters
rewrite/     rewriting/summarization/translation
scheduler/   periodic background jobs
storage/     SQLite/JSON persistence
config.py    YAML + environment configuration
logging.py   console/file logging
engine.py    lifecycle manager
```

## Pipeline

The documented default scheduler pipeline is:

```text
fetch -> models/storage -> rewrite -> publisher
```

with outputs for Eitaa, RSS and PWA-compatible endpoints.

## Aggregation

The project documents source priority/weighting, reliability scoring, failure isolation, duplicate detection and content merge.

## Security

API security includes IP-based rate limiting, API keys/session tokens, role-based permissions and security headers.

## Configuration

Configuration precedence is defaults -> YAML -> `YASINFEED_` environment overrides, with nested keys represented using double underscores.

## Testing / Deployment

Tests use Python unittest. Deployment documentation targets Linux and Termux and includes process-management/security guidance.

## Boundary

YasinFeed must not become YasinHub, Yasin-Agent or YasinCLI. AI/model integrations should remain adapter-based rather than embedding heavy agent frameworks into the core.

## Audit Status

**Level 3:** module, pipeline, boundary, security and configuration architecture are strongly documented. Exact API contracts, provider dependencies and cross-project integrations require source audit.
