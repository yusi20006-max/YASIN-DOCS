# YasinRelay — Public API & Pipeline Contract v1

## Evidence

Source-verified against `yusi20006-max/YasinRelay` README, `yasinrelay/ai_processor.py`, and `yasinrelay/pipeline_engine.py`.

Repository release identified by README: **v2.0.0 Stable**.

## 1. Role

YasinRelay is a content relay pipeline that receives Telegram content, normalizes and validates it, detects duplicates, optionally processes it with AI, prepares media, and publishes to Eitaa.

The v2 architecture explicitly defines:

```text
Collector
  ↓
Normalizer
  ↓
Validator
  ↓
Duplicate Detection
  ↓
AI Processing
  ↓
Media Processing
  ↓
Publisher
```

The repository also uses local SQLite storage, scheduling, structured logging, and a Go fetcher subprocess. fileciteturn183file0

## 2. AI Processing Contract

### Contract ID

`RELAY-AI-PROCESSOR`

### Source-verified public types

```text
ProcessedContent
ContentProcessor
AIProcessor
PassthroughProcessor
CallableProcessor
```

### `ProcessedContent`

Fields:

```python
source_post: Post
text: str
summary: Optional[str]
```

### `ContentProcessor`

Abstract method:

```python
process(post: Post) -> ProcessedContent
```

### `AIProcessor`

Extends `ContentProcessor` and requires:

```python
summarize(text: str) -> str
rewrite(text: str) -> str
translate(text: str, target_lang: str = "persian") -> str
generate_title(text: str) -> str
```

The source explicitly confirms this as an abstraction boundary rather than a dependency on a specific AI platform. fileciteturn185file0

### `PassthroughProcessor`

Constructor:

```python
PassthroughProcessor(
    api_key: str = "",
    base_url: str = "https://api.openai.com/v1",
    model: str = "gpt-4o-mini",
)
```

It can call an OpenAI-compatible `/chat/completions` endpoint and falls back to the original post text when no key is configured or processing fails.

This is an important architectural boundary:

```text
YasinRelay
    ↓
ContentProcessor / AIProcessor
    ↓
provider implementation
```

It does **not** prove:

```text
YasinRelay → Yasin-AI
```

## 3. Callable Processor

`CallableProcessor` accepts:

```python
CallableProcessor(transform: Callable[[str], str])
```

and converts the callable result into `ProcessedContent`.

This provides a lightweight adapter mechanism for alternate AI/local/API backends without changing the pipeline stages. fileciteturn185file0

## 4. Pipeline Contract

### Contract ID

`RELAY-PIPELINE`

### Core types

```text
PipelineContext
PipelineStage
CollectorStage
NormalizerStage
ValidatorStage
DuplicateDetectionStage
AIProcessorStage
MediaProcessorStage
PublisherStage
```

### `PipelineContext`

Source-verified fields:

```text
post: Post
processed_text: str
processed_media_url: Optional[str]
is_duplicate: bool
is_valid: bool
published_success: bool
metadata: Dict[str, Any]
errors: List[str]
```

It initializes processed text/media from the source `Post` when not explicitly supplied. fileciteturn186file0

### `PipelineStage`

Abstract contract:

```python
process(context: PipelineContext) -> PipelineContext
```

Each stage mutates/returns the pipeline context while respecting invalid or duplicate states.

## 5. Collector Contract

`CollectorStage` receives a `FetchEngine` and optional `EventBus`.

Source-verified public operation:

```python
collect(channel: str, limit: int = 10) -> List[PipelineContext]
```

It converts fetched `Post` objects into pipeline contexts and emits content-received events.

## 6. Normalizer Contract

`NormalizerStage.process(context)` strips surrounding whitespace from processed text and emits the normalized-content event.

It does not process invalid or duplicate contexts.

## 7. Validator Contract

`ValidatorStage.process(context)` rejects a post when both processed text and processed media are empty.

Invalid contexts receive an error entry and are not passed into later processing as valid work.

## 8. Deduplication Contract

### Function

```python
calculate_content_hash(
    text: str,
    media_url: Optional[str] = None,
) -> str
```

The implementation uses SHA-256 over text and optional media URL.

### Database boundary

`DuplicateDetectionStage` can use a `Database` to:

```text
exists(...)
save_post(...)
```

New posts are initially recorded as `pending`; duplicates are marked in the pipeline context.

## 9. AI Stage Contract

`AIProcessorStage` accepts a `ContentProcessor` rather than requiring an `AIProcessor` specifically.

Source-verified constructor shape:

```python
AIProcessorStage(
    processor: ContentProcessor,
    event_bus: Optional[EventBus] = None,
)
```

It creates a temporary `Post`, invokes `processor.process()`, and writes the resulting text/summary into `PipelineContext`.

AI exceptions are recorded in `context.errors`; the pipeline does not automatically discard the original content.

## 10. Media Stage Contract

`MediaProcessorStage` accepts a `MediaProcessor` and invokes its image-processing boundary when media is present.

The resulting media URL is stored back into `PipelineContext`.

## 11. Publisher Contract

`PublisherStage` accepts:

```text
EitaaPublisher
Database
EventBus (optional)
```

It builds `ProcessedContent`, publishes through the Eitaa publisher, updates `published_success`, and marks the database record as published when successful.

This confirms:

```text
Pipeline → EitaaPublisher
```

as an application-local publishing boundary.

## 12. Event Contract

The pipeline source defines events including:

```text
EVENT_CONTENT_RECEIVED
EVENT_CONTENT_NORMALIZED
EVENT_DUPLICATE_DETECTED
EVENT_PROCESSING_STARTED
EVENT_AI_PROCESSING_COMPLETED
EVENT_MEDIA_PROCESSING_COMPLETED
EVENT_PUBLISHING_STARTED
EVENT_PUBLISHING_COMPLETED
EVENT_PROCESSING_FAILED
```

These events are internal pipeline observability/integration points unless an external contract is explicitly defined.

## 13. Operational Interface

The README documents three execution modes:

```text
python3 -m yasinrelay.cli run
python3 -m yasinrelay.cli run --schedule
python3 -m yasinrelay.cli run --loop
```

Additional controls include per-channel and limit selection. fileciteturn183file0

## 14. External Provider Boundary

Current documented AI configuration:

```text
AI_PROVIDER
AI_API_KEY
AI_BASE_URL
AI_MODEL
```

Default values include an OpenAI-compatible base URL and model. This is a provider configuration boundary, not evidence of a mandatory dependency on OpenAI or Yasin-AI.

## 15. Architecture Boundary

```text
Telegram
   ↓
Go Fetcher / FetchEngine
   ↓
PipelineContext
   ↓
Normalizer
   ↓
Validator
   ↓
Deduplication ↔ SQLite
   ↓
ContentProcessor / AIProcessor
   ↓
MediaProcessor
   ↓
EitaaPublisher
   ↓
Eitaa
```

YasinRelay owns this relay/publishing pipeline.

It should not become the owner of ecosystem-wide AI runtime, agent orchestration, or shared memory merely because it consumes an AI provider.

## 16. Contract Status Update

`RELAY-AI-PROCESSOR`

**Source verified.**

`RELAY-PIPELINE`

**Source verified.**

`RELAY-PUBLISHER`

**Source verified at the integration-boundary level.** Exact publisher method schema should be extracted in the next deeper audit.

## 17. AI Agent Rules

When modifying YasinRelay:

1. Preserve `ContentProcessor` as the provider-neutral processing boundary.
2. Do not hard-code Yasin-AI as the AI backend unless a new explicit contract/adapter is introduced.
3. Preserve pipeline stage ordering unless an ADR approves an architectural change.
4. Keep deduplication state in Relay's storage boundary.
5. Do not treat pipeline events as external APIs without an explicit contract.
6. Preserve graceful AI failure behavior unless deliberately changing reliability semantics.
7. Update the Contract Registry when public abstractions change.
8. Update project architecture documentation when stage ownership changes.

## 18. Open Work

Next source extraction should cover:

```text
fetch_engine.py
media_processor.py
eitaa_publisher.py
event_bus.py
storage/database.py
cli.py
scheduler.py
```

The purpose is to capture exact provider/publisher signatures, event payload schemas, database contracts, and CLI exit/error semantics.

## Status

**YasinRelay Public API & Pipeline Contract v1 — source-verified baseline complete.**
