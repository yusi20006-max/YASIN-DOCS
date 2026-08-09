# Phase 8 — Source Verification Report

- Date: 2026-08-09
- Scope: Yasin ecosystem ADRs 0001–0011
- Verification mode: repository-level source/documentation inspection
- Status: Initial verification pass

## 1. Purpose

This document compares architectural intent in the ADR set with repository evidence.

Results use four levels:

- **CONFIRMED** — repository evidence directly supports the ADR decision.
- **PARTIAL** — the direction is supported, but the ADR is broader than current evidence.
- **CONFLICT** — repository evidence materially contradicts the ADR wording.
- **UNVERIFIED** — insufficient evidence was inspected.

An ADR must not be marked `Accepted` solely because it is internally coherent.

## 2. Repositories inspected

| Repository | Evidence | Result |
|---|---|---|
| Yasin-core | `README.md` | Strong foundation/runtime evidence |
| Yasin-agent | `README.md` | Strong agent/workflow evidence |
| Yasin-AI | `README.md` | Strong AI platform evidence; plugin trust explicitly limited |
| YasinHub | `README.md` | Status/monitoring evidence; broader control-plane wording needs narrowing |
| YasinRelay | `README.md` | Strong relay/pipeline evidence; also contains AI processing and publishing |
| Yasinfeed | `README.md` | Strong collection/processing/publishing evidence |
| Yasin-cli | `README.md` on `initial-setup` | Strong standalone CLI/control-surface evidence; cross-component integration needs verification |
| YASIN-DOCS | ADR/index documents | Documentation-governance evidence |

## 3. ADR Verification Matrix

| ADR | Decision | Result | Main Finding |
|---|---|---|---|
| 0001 | Multi-repository ecosystem | CONFIRMED | Multiple repositories have explicit project identities and boundaries. |
| 0002 | Core runtime boundary | CONFIRMED | Core explicitly identifies itself as the central runtime layer and lists runtime/SDK foundations. |
| 0003 | Agent orchestration separated from Core | PARTIAL | Yasin-Agent owns planning/execution/tool/workflow behavior, but Core also contains `agents/` and `execution/`; the boundary is layered, not absolute. |
| 0004 | YasinHub management boundary | PARTIAL | Current Hub is explicitly a lightweight status CLI with status store, process checker, registry, and report. Broader control-plane wording is ahead of verified implementation. |
| 0005 | YasinRelay pipeline boundary | CONFIRMED | Relay documents Collector→Normalizer→Validator→Dedup→AI→Media→Publisher plus SQLite, scheduler, and CLI. |
| 0006 | YasinCLI control surface | PARTIAL | CLI has config/doctor/status/service/plugin control capabilities. Direct integration with all named Yasin components is not established by the inspected README. |
| 0007 | Yasin-AI provider/AI boundary | PARTIAL | Yasin-AI is an AI platform, but Core also exposes provider interfaces and Relay/Feed contain AI integration points. Boundary should be capability-oriented, not exclusive. |
| 0008 | Component-scoped storage ownership | PARTIAL | Core, AI, Relay, and Feed document persistence boundaries. Cross-project database access was not sufficiently inspected to prove the full ecosystem rule. |
| 0009 | Explicit security/trust boundaries | CONFIRMED | Yasin-AI explicitly states plugin execution is trusted/in-process and untrusted remote plugin execution is unsupported. |
| 0010 | Feed/content/publishing boundaries | CONFLICT / NEEDS REWRITE | YasinFeed owns collection, processing, and publishing; YasinRelay also performs AI processing, media preparation, and final Eitaa publishing. |
| 0011 | Centralized documentation governance | CONFIRMED | YASIN-DOCS contains the ecosystem ADR system and central architecture/documentation governance. |

## 4. Critical Findings

### 4.1 ADR-0010 requires correction

Current evidence shows both:

```text
YasinFeed
  fetch → process/rewrite → publish
```

and:

```text
YasinRelay
  collect → normalize → validate → deduplicate → AI → media → publish
```

The ecosystem therefore currently contains overlapping pipeline/application responsibilities. ADR-0010 should not claim strict exclusive separation until ownership is clarified or implementation is refactored.

### 4.2 ADR-0004 is broader than current Hub implementation

Verified Hub responsibilities are closer to:

```text
status store
+ process checking
+ project registry
+ status report
+ CLI status command
```

The phrase “primary ecosystem management/control boundary” should be treated as target architecture unless additional source evidence confirms more capabilities.

### 4.3 ADR-0003 needs a layered boundary model

Yasin-Core contains agent/runtime/execution packages, while Yasin-Agent provides a higher-level agent platform with planner, executor, tools, memory/context, sessions, and Core SDK integration.

A better verified distinction is:

```text
Yasin-Core
  = foundational runtime primitives / shared execution infrastructure

Yasin-Agent
  = higher-level agent definition / workflow / orchestration platform
```

### 4.4 ADR-0007 should avoid exclusive ownership language

Yasin-Core documents provider interfaces/adapters, while Yasin-AI documents an AI platform and Relay/Feed contain AI processing integration points.

The safest verified model is:

```text
Core
  └─ low-level provider/runtime interfaces

Yasin-AI
  └─ reusable AI platform/capabilities

Consumers
  └─ domain-specific AI adapters/workflows
```

## 5. Acceptance Recommendation

| ADR | Recommendation |
|---|---|
| 0001 | Accept after normal maintainer review |
| 0002 | Accept after confirming public API scope |
| 0003 | Revise wording, then review |
| 0004 | Revise current-state vs target-state wording |
| 0005 | Accept after checking relay contracts |
| 0006 | Revise integration claim; retain control-surface decision |
| 0007 | Revise capability/provider wording |
| 0008 | Keep Proposed until storage schemas and cross-project access are audited |
| 0009 | Accept principle; maintain implementation-specific threat model separately |
| 0010 | **Do not accept yet; rewrite required** |
| 0011 | Accept after governance review |

## 6. Next Verification Pass

Inspect actual source/configuration/tests for:

1. Yasin-Core public API, provider, and storage modules.
2. Yasin-Agent Core integration and execution ownership.
3. YasinHub status/control implementation.
4. YasinRelay pipeline, storage, AI, and publisher modules.
5. YasinFeed scheduler/engine/publisher/storage modules.
6. YasinCLI component integration/service definitions.
7. Yasin-AI plugin/provider/persistence boundaries.

Only after this pass should ADRs move from `Proposed` to `Accepted`.

## 7. Source-of-Truth Rule

```text
Source Code / Tests / Configuration
        ↓
Implementation Reality

Architecture Docs / ADRs
        ↓
Architectural Intent and Rationale

YASIN-DOCS
        ↓
Ecosystem-Level Knowledge / Governance
```

When these disagree, the disagreement is an architectural finding, not something to hide by silently rewriting documentation.
