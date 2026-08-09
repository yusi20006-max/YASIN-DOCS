# Yasin Ecosystem — Event, Message & Data Flow Graph

**Phase:** 6 — System Graphs  
**Status:** Refinement pass 5

## 1. Purpose

This document models how information moves through the Yasin ecosystem. It distinguishes verified producer/consumer relationships from conceptual flows and does not invent a shared event bus or transport protocol.

## 2. Canonical Content Flow

```text
External Sources
  │
  ├── RSS / feeds
  ├── web/content sources
  └── messaging/publishing sources
          │
          ▼
   Ingestion / Fetching
          │
          ▼
 Normalization / Validation
          │
          ▼
 Deduplication / Filtering
          │
          ▼
 AI / Rewrite / Enrichment
          │
          ▼
 Content Model / Storage
          │
          ▼
 Publishing / Distribution
```

This is the ecosystem-level logical flow. It is not a claim that one repository implements every stage.

## 3. FeedBridge Flow

The strongest concrete message boundary currently documented is the local fetcher contract:

```text
FeedBridge Fetch Engine
        │
        │ subprocess
        ▼
Vendored Fetcher
        │
        │ stdout
        ▼
JSON Payload
        │
        ▼
FeedBridge Processing
```

This is a process/message contract rather than an HTTP API.

## 4. Agent Task Flow

```text
Agent Definition
      │
      ▼
Planner
      │
      ▼
Task
      │
      ▼
State Machine
      │
      ▼
Executor
      │
      ├── Tool Runner
      ├── validation
      └── retry
      │
      ▼
Task Result
```

The Agent/Core boundary can provide task creation/execution capabilities, but the exact transport must remain distinct from the logical task flow.

## 5. Relay / Content Processing Flow

```text
Source
  ↓
Relay ingestion
  ↓
Normalization
  ↓
Validation
  ↓
Deduplication
  ↓
AI processing
  ↓
Media / enrichment
  ↓
Publication
```

The stages represent the documented Relay processing responsibilities. They should not be interpreted as separate network services unless source evidence proves process separation.

## 6. Hub / Management Event Flow

```text
Runtime Components
       │
       ├── health/status
       ├── service state
       ├── events
       └── logs
              │
              ▼
           YasinHub
              │
              ▼
       Registry / Dashboard
```

This is a management-data model. The exact transport and event schema remain open.

## 7. CLI Control Flow

```text
User Command
     │
     ▼
YasinCLI Parser
     │
     ▼
Command / Adapter
     │
     ├── discovery
     ├── lifecycle
     ├── health
     ├── logs
     └── status
     │
     ▼
Target Runtime / Management API
```

A CLI command is a control message. It should not be treated as application data.

## 8. Data Classes

The ecosystem can be modeled using these data classes:

### Control data

- start/stop/restart;
- health/status;
- configuration changes;
- discovery requests;
- administrative commands.

### Task data

- task definitions;
- execution state;
- workflow steps;
- tool calls;
- results;
- errors/retry state.

### Content data

- source items;
- normalized articles/items;
- rewritten/enriched content;
- media metadata;
- publication records.

### Management data

- service registration;
- health records;
- events;
- logs;
- capabilities.

### Knowledge data

- memory/context;
- knowledge records;
- retrieval results;
- embeddings or related representations where implemented.

## 9. Transport Classification

Potential transports are intentionally separated:

```text
In-process
  → Python/Node function or SDK call

Subprocess
  → stdin/stdout/stderr contract

HTTP/API
  → request/response contract

WebSocket
  → streaming/session contract

Queue/Event Bus
  → asynchronous message contract

File
  → artifact/config/data contract

Database
  → persistent data contract
```

Only use a transport label when source evidence supports it.

## 10. Event Bus Rule

There is **no ecosystem-wide event bus assumption**.

If YasinHub, YasinRelay, or another project implements events, those events are project-local until an external producer/consumer and transport are verified.

## 11. Message Schema Rule

A message contract is not considered stable merely because two components exchange JSON.

A stable contract requires, where applicable:

- schema/version;
- required fields;
- optional fields;
- validation rules;
- error semantics;
- compatibility policy;
- producer ownership;
- consumer ownership.

## 12. Failure / Retry Flow

```text
Producer
   │
   ▼
Transport / Boundary
   │
   ├── validation failure ──► reject / error
   ├── transient failure ───► retry where supported
   └── success ─────────────► consumer
```

Retry behavior is component-specific and must not be generalized across the ecosystem.

## 13. Data Ownership Rule

For every cross-project flow, future documentation should identify:

```text
Producer
Consumer
Data owner
Schema owner
Transport owner
Validation owner
Persistence owner
Retention owner
Security classification
```

## 14. Current Evidence Gaps

- complete cross-project API payload schemas;
- Hub event schemas and transport;
- Relay event/message interfaces;
- Feed publication message contracts;
- exact Core task payload schema;
- exact CLI-to-service transport per adapter;
- queue/broker usage;
- WebSocket usage;
- persistent event storage;
- replay/idempotency guarantees.

## 15. AI Maintenance Rule

Never invent an event name, topic, queue, endpoint, JSON field, or schema version. If it has not been verified, document the flow at the capability level and mark the transport/schema as unknown.
