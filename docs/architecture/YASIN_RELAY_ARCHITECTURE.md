# YasinRelay — Ecosystem Architecture

## Role

YasinRelay is the content-ingestion and publishing pipeline of the Yasin ecosystem. Its current primary flow is Telegram → processing → Eitaa.

## Core Pipeline

```text
Telegram Channels
       │
       ▼
Collector / Fetch Engine
       │
       ▼
Normalizer
       │
       ▼
Validator
       │
       ▼
Duplicate Detection
       │
       ▼
AI Processor
       │
       ▼
Media Processor
       │
       ▼
Publisher
       │
       ▼
Eitaa
```

The v2 engine is modular and uses a `PipelineContext` to carry processed text, media, duplicate state, validation state, publication state, metadata, and errors between stages.

## AI Boundary

YasinRelay defines an `AIProcessor` abstraction with operations for summarization, rewriting, translation, title generation, and processing. The current `PassthroughProcessor` is API-compatible with OpenAI-style chat completions and can fall back to passthrough behavior when no API key is configured. A callable processor also permits arbitrary backends without changing the rest of the pipeline.

Therefore:

```text
YasinRelay
   │
   └── AIProcessor interface
           │
           ├── OpenAI-compatible HTTP backend
           ├── Callable/custom backend
           └── Future Yasin-AI integration (NOT currently proven)
```

No direct dependency on `Yasin-AI` was found in the inspected source. Do not document one as a runtime dependency without source evidence.

## Persistence

SQLite stores posts and supports duplicate detection and publication state. This is Relay-owned operational persistence, not a claim that Relay owns ecosystem-wide memory.

## Event Boundary

The pipeline publishes events for content reception, normalization, duplicate detection, AI processing, media processing, publishing start/completion, and failures. This is an internal loose-coupling mechanism inside Relay; it should not be confused with an ecosystem-wide event bus until a formal external contract exists.

## Scheduler

Relay includes a lightweight local scheduler and supports single-run, scheduled, and legacy loop execution modes.

## Ecosystem Position

```text
                 YasinHub / YasinCLI
                         │
                    lifecycle
                         │
                         ▼
                    YasinRelay
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      Telegram       AI Processor     SQLite
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                      Eitaa
```

Hub/CLI control Relay operationally; Relay owns its own content pipeline.

## Architectural Constraints

1. Keep ingestion, transformation, storage, and publication boundaries explicit.
2. Keep AI behind `AIProcessor` so provider changes do not rewrite the pipeline.
3. Do not make Relay depend directly on Yasin-AI until a deliberate integration contract is designed.
4. Treat Relay SQLite as pipeline state, not ecosystem memory.
5. Treat internal Relay events as local events unless promoted to a documented ecosystem protocol.

## Audit Status

- Pipeline role: **CONFIRMED**
- AI abstraction: **CONFIRMED**
- SQLite operational state: **CONFIRMED**
- Scheduler: **CONFIRMED**
- Direct Yasin-AI dependency: **NOT CONFIRMED**
- Hub/CLI operational control: **CONFIRMED at ecosystem architecture level**
