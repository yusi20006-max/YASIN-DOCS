# Yasin Ecosystem — Storage & Schema Audit

**Phase:** 6 — System Graphs  
**Status:** Consolidated source-evidence pass

## Purpose

Create a single source-of-truth map for persistent state, schema ownership, and configuration-backed storage. This document deliberately separates verified implementation from architectural intent.

## Verified Storage Evidence

### Yasin-AI

The repository documents **local SQLite-backed persistent storage** as the default persistence model. It explicitly does not claim distributed/high-availability storage or automatic multi-node failover. 

### YasinRelay

The repository documents a **local SQLite database**, with `DATABASE_PATH` defaulting to `relay.db`. Its package structure contains a dedicated `storage/` layer for SQLite and models.

### YasinHub

The documented status model uses JSON status files and combines those files with live process checks. `status_store.py` is responsible for reading/writing JSON status files. This is a file-backed status store, not evidence of a shared relational database.

## Storage Ownership Matrix

| Project | Verified persistence | Owner | Shared-store evidence |
|---|---|---|---|
| Yasin-Core | Architecture requires verification | Core | None established |
| Yasin-Agent | Session/context behavior documented; exact persistence requires verification | Agent | None established |
| Yasin-AI | Local SQLite | Yasin-AI | None established |
| YasinHub | JSON status files | YasinHub | None established |
| YasinRelay | SQLite (`relay.db` default) | YasinRelay | None established |
| YasinFeed | Requires source-level verification | YasinFeed | None established |
| YasinPress | Requires source-level verification | YasinPress | None established |

## Schema Ownership Rules

A schema belongs to the component that owns the persistence lifecycle unless an explicit external schema owner is documented.

Schema ownership includes:

- field definitions;
- validation;
- migrations;
- compatibility;
- retention;
- backup/restore semantics;
- cleanup;
- data lifecycle.

## Important Distinction

```text
Storage technology
    ≠
Data schema
    ≠
API schema
    ≠
Message schema
```

A SQLite database does not by itself define an API contract. Likewise, JSON status files do not establish an ecosystem-wide JSON protocol.

## Remaining Source Audit

The following must be inspected directly before being marked verified:

- Yasin-Core storage implementation and schema/migration mechanism;
- Yasin-Agent context/session persistence implementation;
- Yasin-Feed storage implementation;
- Yasin-Press storage implementation;
- Yasin-AI table/schema definitions;
- YasinRelay SQLite schema/migrations;
- YasinHub JSON status schema;
- retention and cleanup policies;
- backup/restore procedures.

## AI Maintainer Rule

Never alter a persistent schema merely to satisfy a failing test without checking migration, backward compatibility, existing data, and rollback impact.
