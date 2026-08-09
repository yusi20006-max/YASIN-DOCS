# Yasin Ecosystem — Dependency & Contract Graph

**Phase:** 6 — System Graphs  
**Status:** Refinement pass 1

## Purpose

This document separates four different kinds of relationships so future AI agents do not confuse them:

1. package/import dependency;
2. process/runtime integration;
3. API producer/consumer contract;
4. conceptual capability relationship.

Only relationships with sufficient evidence are marked **verified**.

## 1. High-Confidence Dependency/Integration Map

```text
Yasin-Agent
    │
    │ SDK / adapter integration
    ▼
Yasin-Core

YasinCLI
    │
    ├── lifecycle/control integration ──► Yasin-Core
    ├── lifecycle/control integration ──► Yasin-Agent
    ├── management integration ─────────► YasinHub
    └── service integration ─────────────► YasinRelay

FeedBridge
    │
    └── local subprocess ────────────────► vendored fetcher

Yasin-AI
    │
    └── executable entry point: yasin
```

The arrows above do not all have the same technical mechanism. The mechanism must be read from the labels and the project's own contract documents.

## 2. Package Dependency vs Runtime Dependency

### Package dependency

A package dependency exists only when a manifest or source import establishes it.

### Runtime dependency

A runtime dependency may exist even when no language package dependency exists, for example:

```text
CLI → executable/service
CLI → HTTP API
CLI → subprocess
```

YasinCLI's relationship with the other Yasin components should therefore not be represented as Python/Node package imports unless source evidence proves such imports.

## 3. API Producer / Consumer Model

### Current verified/partially verified contracts

```text
Yasin-Agent
    │ consumer
    ▼
Yasin-Core SDK
    │ provider
    ▼
Core Runtime / Memory / Execution surfaces
```

```text
FeedBridge Fetcher
    │ producer
    │ JSON stdout
    ▼
FeedBridge Fetch Engine
    │ consumer
```

```text
Yasin-AI
    │ provider
    ▼
`yasin` CLI entry point
```

These are deliberately minimal. An API symbol-level graph is not claimed until the corresponding source files are enumerated.

## 4. Storage Ownership — Current Evidence Model

Storage ownership must be assigned to the component that creates, migrates, and reads the persistent store, not merely to a component that happens to consume its data.

Current documentation indicates persistence in multiple projects, including Core, Relay, Feed, and Press. Therefore the architecture must treat these as **separate storage domains until proven otherwise**.

```text
Yasin-Core   → Core-owned persistence boundary
YasinRelay   → Relay-owned persistence boundary
YasinFeed    → Feed-owned persistence boundary
YasinPress   → Press-owned persistence boundary
```

No shared database is assumed.

## 5. Configuration Ownership

Configuration should follow the same ownership rule:

```text
Component
   │
   ├── owns configuration schema
   ├── owns defaults
   ├── owns validation
   └── consumes secrets through its documented runtime boundary
```

A `.env` or YAML file appearing in a repository does not automatically mean another Yasin project owns that configuration.

## 6. Runtime Process Graph

The current evidence supports different runtime classes:

```text
Library
  └── Yasin-Core

Agent / oneshot
  └── Yasin-Agent

Management / oneshot or CLI-driven
  └── YasinHub

Daemon / service
  └── YasinRelay

CLI
  └── YasinCLI

Developer automation
  └── TJC
```

Exact process supervisors, ports, sockets, queues, and deployment hosts remain unverified unless directly documented.

## 7. Event / Message Transport

No universal event bus is assumed for the ecosystem.

Where a project has an explicit event system, it is treated as a project-local capability until an external consumer is verified.

This prevents a future agent from inventing an ecosystem-wide message bus simply because several repositories mention events.

## 8. Trust Boundaries

The architecture currently contains at least these conceptual trust boundaries:

```text
External Internet / Feeds
          │
          ▼
Collection / Ingestion
          │
          ▼
Normalization / Validation
          │
          ▼
AI / Processing
          │
          ▼
Publishing / External Services
```

And for developer operations:

```text
Developer
   │
   ▼
CLI / Automation
   │
   ▼
Local Runtime / GitHub / External APIs
```

These are security architecture boundaries, not claims about a single deployed network topology.

## 9. Unknowns That Must Stay Explicit

- complete import graph across repositories;
- exact Core public symbol set consumed by Agent;
- exact Hub consumers and transport;
- exact CLI adapters and process invocation implementations;
- shared vs isolated storage in every application;
- external API endpoint contracts;
- event payload schemas;
- deployment/service-discovery topology;
- authentication and authorization edges;
- secret ownership and rotation model.

## 10. Graph Quality Rule

Never turn:

```text
mentions
```

into:

```text
depends_on
```

Never turn:

```text
same capability
```

into:

```text
shared implementation
```

Never turn:

```text
roadmap intent
```

into:

```text
current runtime behavior
```

These rules are mandatory for AI-assisted maintenance of YASIN-DOCS.
