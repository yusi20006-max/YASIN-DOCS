# Yasin Ecosystem — System Graphs

**Phase:** 6 — System Graphs  
**Status:** Initial graph baseline  
**Rule:** Solid relationships are evidence-backed; conceptual relationships are explicitly marked.

## 1. Ecosystem Control Graph

```text
User / Operator
      │
      ▼
   YasinCLI
      │
      ├──────────────► Yasin-Core
      ├──────────────► Yasin-Agent
      ├──────────────► YasinHub
      └──────────────► YasinRelay
```

YasinCLI is the ecosystem control-plane candidate and has documented lifecycle/integration responsibilities. Exact transport for every edge remains source-audit dependent.

## 2. Agent Graph

```text
Yasin-Agent
    │
    │ documented SDK integration
    ▼
Yasin-Core
    │
    ├── Runtime
    ├── Context / Memory
    ├── Tools / Plugins
    └── Execution
```

The Agent/Core relationship is evidence-backed. Exact symbol-level API contracts remain to be documented.

## 3. Content / Feed Graph

```text
Telegram / RSS / External Feeds
             │
             ▼
      Feed / Collection Layer
       ├───────────────┐
       ▼               ▼
   OpenFeed         YasinFeed
       │               │
       │               ├── processing
       │               └── publishing
       ▼
   FeedBridge
       │
       └── vendored fetcher → JSON stdout → fetch engine

YasinPress is a separate news-processing application path and must not be treated as a proven runtime child of YasinFeed.
```

## 4. Relay Graph

```text
Sources
  │
  ▼
YasinRelay
  ├── Collect
  ├── Normalize
  ├── Validate
  ├── Deduplicate
  ├── AI Processing
  ├── Media
  └── Publish
```

The exact relationship between Relay and OpenFeed/FeedBridge must be represented according to implementation evidence, not repository naming.

## 5. AI Graph

```text
Yasin-Agent / Applications
          │
          ▼
      AI Capability
          │
          ▼
       Yasin-AI
       ├── Runtime
       ├── Knowledge
       ├── Developer Platform
       ├── Security Platform
       ├── API Service
       └── Observability
```

This is a conceptual capability graph. It does not claim that every application imports Yasin-AI directly.

## 6. Management Graph

```text
YasinCLI
   │
   ▼
YasinHub
   ├── Service Registry
   ├── Health
   ├── Events
   ├── Logs
   └── Dashboard / Management
```

The CLI-to-Hub relationship is an integration boundary, not a package dependency unless source code proves otherwise.

## 7. Supporting Infrastructure Graph

```text
TJC
 │
 └── Developer automation / Jules workflows

Termux Backup Manager
 │
 └── Operational backup / restore / migration

YASIN-DOCS
 │
 └── Architecture / knowledge / AI handoff
```

These are ecosystem-supporting tools, not automatically runtime dependencies.

## 8. Memory / Knowledge Graph

```text
Agent / Application
        │
        ▼
Context + Memory
   ├── Yasin-Core runtime capabilities
   └── Yasin-AI knowledge capabilities
```

This remains a capability graph until all storage and API boundaries are verified.

## 9. Deployment Graph

```text
Developer / Operator
        │
        ├── YasinCLI
        ├── TJC
        └── Backup Manager

Runtime Environment
        ├── Yasin-Core
        ├── Yasin-Agent
        ├── YasinHub
        ├── YasinRelay
        ├── YasinFeed
        └── YasinPress
```

Actual process topology, containers, hosts, ports, queues, and service discovery are not claimed here unless implementation evidence exists.

## 10. Graph Confidence Rules

- **Verified:** direct repository/source/configuration evidence.
- **Documented:** repository documentation explicitly states the relationship.
- **Conceptual:** architectural capability or intended relationship; not proven runtime coupling.
- **Unknown:** evidence is insufficient.

Never convert a conceptual edge into a dependency without source evidence.

## 11. Next Graph Refinement

The next refinement should add:

1. import-level dependency edges;
2. API producer/consumer edges;
3. storage ownership;
4. configuration ownership;
5. runtime process boundaries;
6. event/message flows;
7. deployment topology;
8. security trust boundaries.
