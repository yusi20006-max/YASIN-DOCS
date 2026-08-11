# YasinPress API Contract

Status: Architecture contract / implementation target

This document defines the stable boundary between the YasinPress backend and independent clients such as the PWA. Clients must use the service/API boundary and must not depend on SQLite internals or Python implementation details.

## Design rules

- API responses are JSON.
- Timestamps are ISO-8601 with explicit timezone information; UTC is preferred internally.
- `news_id` is immutable and globally unique within YasinPress.
- Secrets/tokens are never returned by the API.
- Read endpoints must remain usable while individual RSS sources are degraded.
- Mutating/admin endpoints require authentication and authorization.
- Pagination is required for article, queue, log, and report collections.
- The API exposes operational state; it does not expose database implementation details.

## Core endpoints

### `GET /api/status`

Returns application status, version, uptime, scheduler state, queue counts, AI state, publisher state, and current hourly publishing usage.

### `GET /api/health`

Returns component health for database, internet connectivity, RSS manager, AI, publisher, scheduler, watchdog, and API.

### `GET /api/sources`

Returns configured/discovered RSS sources and health metadata: name, URL, enabled state, priority, status, last success, last failure, response time, article counts, and error count.

### `GET /api/articles`

Paginated article listing. Supports filtering by source, category, status, freshness, priority, breaking flag, AI state, and date range.

### `GET /api/articles/{news_id}`

Returns the normalized article, intelligence metadata, event association, processing history, and publication state.

### `GET /api/queue`

Returns persistent publication queue state, including pending, processing, retrying, failed, and dead-letter jobs.

### `GET /api/publishing`

Returns publisher status, hourly quota usage, recent successes/failures, and current delivery statistics.

### `GET /api/metrics`

Returns time-series operational metrics suitable for PWA charts.

### `GET /api/reports/hourly`

Returns hourly operational reports, including received, accepted, rejected, duplicate, AI-processed, queued, published, failed, source health, queue depth, internet status, and publisher status.

## Administrative endpoints

These are implementation targets and must be protected by authentication:

- `POST /api/sources`
- `PATCH /api/sources/{id}`
- `POST /api/queue/{id}/retry`
- `POST /api/queue/{id}/cancel`
- `POST /api/system/restart`
- `POST /api/system/reload`

## Article contract

```json
{
  "news_id": "YP-260812-483721",
  "event_id": "EV-260812-0192",
  "source": {
    "id": "bbc-persian",
    "name": "BBC Persian",
    "article_url": "..."
  },
  "title": "...",
  "summary": "...",
  "published_at": "2026-08-12T10:30:00Z",
  "received_at": "2026-08-12T10:32:10Z",
  "age_minutes": 125,
  "category": "world",
  "priority": 82,
  "breaking": false,
  "freshness": "valid",
  "duplicate": false,
  "ai": {
    "enabled": true,
    "rewritten": true,
    "provider": "..."
  },
  "status": "queued"
}
```

## PWA requirements

The PWA must be implementable against this contract using mock data before the backend is complete. Mock responses must preserve field names and semantics so switching to the real API does not require a UI rewrite.

## Compatibility

Breaking API changes require a versioned contract and an architecture decision record. Additive fields are preferred over changing the meaning of existing fields.
