# Phase 8 — YasinRelay Source Audit

- Date: 2026-08-11
- Status: Source-verified audit
- Repository: `yusi20006-max/YasinRelay`
- Scope: runtime pipeline, storage, AI boundary, media handling, publishing, scheduler, and external fetcher

## Executive Finding

YasinRelay is a self-contained application/data pipeline for Telegram-to-Eitaa content delivery. The repository owns the complete application pipeline from collection through normalization, validation, deduplication, AI processing, media preparation, and publishing.

No source evidence was found in the audited files establishing a direct runtime dependency on `Yasin-Core`, `Yasin-Agent`, or `Yasin-AI`.

## Source-Verified Pipeline

```text
Telegram Channels
      |
      v
CollectorStage / FetchEngine
      |
      v
NormalizerStage
      |
      v
ValidatorStage
      |
      v
DuplicateDetectionStage -> SQLite
      |
      v
AIProcessorStage -> local ContentProcessor boundary
      |
      v
MediaProcessorStage
      |
      v
PublisherStage -> EitaaPublisher -> Eitaar API
```

The pipeline engine source explicitly imports and composes `FetchEngine`, `ContentProcessor`, `MediaProcessor`, `Database`, and `EitaaPublisher`.

## Ownership Classification

| Capability | Current owner | Classification | Evidence status |
|---|---|---|---|
| Telegram collection | YasinRelay | `RUNTIME_DEPENDENCY` internal | CONFIRMED |
| Text normalization | YasinRelay | `INTERNAL` pipeline stage | CONFIRMED |
| Content validation | YasinRelay | `INTERNAL` pipeline stage | CONFIRMED |
| Deduplication | YasinRelay + SQLite | `DATA/SCHEMA_DEPENDENCY` internal | CONFIRMED |
| AI processing | YasinRelay | `OPTIONAL_INTEGRATION` / local boundary | CONFIRMED |
| Media preparation | YasinRelay | `INTERNAL` pipeline stage | CONFIRMED |
| Eitaa publishing | YasinRelay | external API integration | CONFIRMED |
| Scheduling | YasinRelay | runtime/application service | CONFIRMED |
| Core SDK | — | no audited dependency | UNVERIFIED |
| Yasin-Agent SDK | — | no audited dependency | UNVERIFIED |
| Yasin-AI platform | — | no audited dependency | UNVERIFIED |
| YasinHub | — | operational/reporting relationship only in current docs | UNVERIFIED as runtime dependency |

## Eitaa Boundary

`EitaaPublisher` owns the application-facing Eitaa publishing integration. The audited implementation builds the API URL from the configured API base, token, and endpoint; selects `sendMessage` for text and `sendFile` when media is present; and records publishing success/failure in the pipeline context.

The publisher also contains rate limiting and media-download fallback behavior. Therefore Eitaa delivery is an application-owned integration boundary, not evidence of ownership by another Yasin project.

## AI Boundary

`AIProcessorStage` receives a local `ContentProcessor` abstraction and invokes it against a temporary `Post` representation. AI failures are recorded in the pipeline context and do not automatically abort the pipeline; the implementation falls back to the existing processed text.

This supports the current dependency-matrix classification of Relay AI as a local application boundary. It does **not** prove that Relay cannot later delegate AI work to Yasin-AI.

## Storage Boundary

`DuplicateDetectionStage` calculates a SHA-256 content hash and uses the Relay `Database` to detect previously seen content and persist pending posts. The storage path is therefore owned by Relay for the audited implementation.

This is relevant to ADR-0008: no evidence from this audit establishes that Relay storage/memory should be delegated to Core or Yasin-AI.

## External Fetcher Boundary

The README documents a Go-based fetcher compiled as `fetcher/openfeed-fetch`. The Eitaa publisher can invoke this binary as a subprocess for media downloads. This is a `CLI/SUBPROCESS_INTEGRATION`, not a Yasin-Core runtime dependency.

## Architectural Rules Confirmed

1. Relay owns its application pipeline.
2. Relay may consume external AI providers without implying Yasin-AI ownership.
3. Relay's SQLite persistence is currently application-local.
4. Eitaa is an external publishing boundary owned by Relay's publisher adapter.
5. The Go fetcher is an implementation dependency of Relay's collection/media path.
6. Core/Agent dependencies must not be inferred from shared concepts or project names.
7. A future integration with Hub/Core/Agent/AI requires an explicit public API, SDK, protocol, or package dependency.

## ADR Impact

- ADR-0006: **CONFIRMED for Relay's application pipeline boundary**, subject to ecosystem-wide audit.
- ADR-0008: **PARTIAL**; Relay-local storage is confirmed, but ecosystem-wide memory/storage ownership remains unresolved.
- ADR-0010: **REQUIRES CROSS-PROJECT REVIEW**; this audit confirms Relay has its own full content-processing/publishing pipeline, so overlap with YasinFeed must be modeled before acceptance.

## Remaining Evidence Gaps

1. Full source audit of Relay configuration and scheduler modules.
2. Direct package/import verification for any optional Yasin ecosystem adapters outside the audited pipeline files.
3. Cross-project comparison with YasinFeed and YasinPress to determine whether Relay's pipeline is intentionally specialized or duplicates shared application responsibilities.
4. Operational integration evidence for YasinHub.

## Next Step

Proceed to the YasinFeed source audit, then compare Relay and Feed side-by-side before changing ADR-0010 or declaring the application-pipeline ownership model final.
