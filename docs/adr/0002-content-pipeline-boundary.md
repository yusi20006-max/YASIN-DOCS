# ADR-0002: Keep Content Collection, Processing and Publishing Inside Domain Pipelines

- **Status:** Accepted
- **Date:** 2026-08-11
- **Scope:** YasinFeed, YasinRelay, YasinPress

## Context

Several Yasin projects operate on content. Their names and historical lineage can make their responsibilities appear interchangeable even when their actual boundaries differ.

YASIN-DOCS already records YasinFeed as a general content collection/processing/publishing engine and YasinRelay as a relay-oriented pipeline. YasinPress Rewrite is a specialized Persian-news application with RSS fetching, processing, categorization, priority/breaking analysis and publishing.

## Decision

Each domain pipeline owns its own content lifecycle:

```text
Source
  ↓
Fetch / Collect
  ↓
Normalize / Validate
  ↓
Process / Classify
  ↓
Optional AI enrichment
  ↓
Publish
```

The control plane may start, stop, inspect and coordinate these applications, but it must not absorb their domain processing logic.

Likewise, one content application must not become a hidden dependency of another merely because both process news/content. Any shared capability should be introduced through an explicit contract and documented dependency.

## Consequences

- Domain logic stays close to the application that owns it.
- YasinFeed, YasinRelay and YasinPress can have different policies while sharing ecosystem conventions.
- Cross-application reuse requires an explicit API/library boundary.
- Historical relationships such as OpenFeed/FeedBridge lineage are documented separately from current ownership.

## Evidence

The YASIN-DOCS project registry records YasinFeed as owning collection, processing and publishing pipes and YasinRelay as a complete content relay pipeline. YasinPress Rewrite has been runtime-verified as a Python application with feed fetching, processing and publishing components.

## Alternatives considered

### Centralize all content processing in YasinHub

Rejected because it would turn the control plane into a business-logic monolith.

### Make YasinPress depend directly on YasinFeed or YasinRelay

Rejected until a source-verified contract demonstrates a real shared interface and the dependency provides clear architectural value.
