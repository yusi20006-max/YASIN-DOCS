# YasinPress Data Model Contract

Status: Architecture contract / implementation target

## Identity

### News ID

Every ingested article receives an immutable identifier:

`YP-YYMMDD-XXXXXX`

The identifier is assigned once and survives restart, retry, deduplication, queue recovery, and publication.

### Event ID

`EV-YYMMDD-XXXX`

An Event ID groups multiple reports about the same real-world event. A single event can contain multiple distinct News IDs when there is meaningful new information.

## Article lifecycle

```text
received
  -> normalized
  -> validated
  -> intelligence
  -> queued
  -> processing
  -> published
```

Alternative terminal/side states:

```text
rejected
duplicate
expired
failed
cancelled
dead_letter
```

## Freshness

Normal articles are eligible when their publication age is at most 12 hours. Articles older than 12 hours are rejected unless they pass the explicit breaking/urgent exception policy. The source publication timestamp, not the local ingestion timestamp, is used for freshness.

A genuinely new update to an existing event receives a new News ID and is evaluated using its new publication/update timestamp.

## AI state

AI processing must be explicit in stored state:

- `disabled`
- `pending`
- `rewritten`
- `fallback_original`
- `failed`

A public message must mark AI-rewritten content with the agreed `🤖` indicator.

## Source state

Each source stores operational health independently:

- enabled/disabled
- healthy/degraded/unavailable
- last successful fetch
- last failure
- response time
- consecutive failures
- received count
- accepted count
- rejected count

One failed source must not stop the global pipeline.

## Queue state

Queue jobs persist:

- News ID
- priority
- scheduled time
- attempts
- last error
- lock/lease information
- state
- timestamps

The queue must survive process restart and recover unfinished work safely.

## Publishing policy

Global publication capacity is limited to 10 messages per hour. Scheduling must be fair across active sources so one source cannot consume the entire hourly capacity. Per-source limits may be configured, with the current target of at most 5 messages per source per hour.

Retries use bounded exponential/backoff behavior and eventually move permanently failing jobs to a dead-letter state.

## Hourly metrics

The canonical hourly report should be derivable from persisted state and include:

- received
- accepted
- rejected
- expired (>12h)
- duplicates
- AI rewritten
- AI fallback
- queued
- published
- failed
- retrying
- queue depth
- active source count
- inactive/degraded source count
- internet status
- AI status
- Eitaa status

These metrics feed both the PWA and the support/report channel so they do not drift into separate sources of truth.
