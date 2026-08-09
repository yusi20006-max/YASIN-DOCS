# FeedBridge — Project Architecture Record

## Evidence Level

**README-verified / source audit pending**

## Identity

Repository: `yusi20006-max/Feedbridge`

## Purpose

FeedBridge is a self-contained Telegram content bridge. It fetches Telegram content using an embedded Go fetcher derived from OpenFeed's proven `telemirror` engine, processes the content, optionally applies AI processing, and publishes to Eitaa.

## Key Architectural Property

FeedBridge does **not** require a separate OpenFeed runtime at runtime. The fetcher is vendored into the repository and built as part of the project.

This distinction is important:

```text
OpenFeed
  └── source/engine lineage
          ↓
FeedBridge vendored fetcher
          ↓
FeedBridge runtime
```

This should not be represented as `FeedBridge → OpenFeed service` unless implementation evidence later proves such a dependency.

## Documented Pipeline

```text
Vendored Fetcher
      ↓
Fetch Engine
      ↓
Duplicate Detector
      ↓
AI Engine
      ↓
Queue Manager
      ↓
Publish Engine
      ↓
Eitaa
```

## Components / Features

- Persistent channel manager
- SQLite database
- Queue system
- Duplicate detection
- AI processing
- Dashboard
- Plugin architecture
- Health monitor
- Logging

## Runtime

- Python 3.14+
- Go 1.22+ for embedded fetcher
- SQLite

The Go fetcher is built inside the repository and invoked as a subprocess. Its JSON stdout is consumed by the Fetch Engine.

## Ownership Implications

FeedBridge owns its application workflow: processing, queueing, publishing and related application management. It should not automatically absorb OpenFeed's stable-core responsibilities or ecosystem-wide management responsibilities.

## Audit Remaining

- Actual Python module structure
- Go/Python subprocess contract
- SQLite schema
- Queue semantics
- Plugin boundaries
- AI provider interface
- Eitaa publisher contract
- Configuration/secrets
- Tests and CI/CD
- Security of subprocess and untrusted content handling
- Relationship with YasinRelay and YasinFeed
