# Yasin Ecosystem — Source-Level API Audit v1

## Purpose

This document records the first implementation-backed pass over the public API surface for the ecosystem contract registry.

The goal is to separate **documented capabilities** from **source-verified public symbols**.

## Evidence Levels

- **S1 — Source verified:** exact source symbol/path was inspected.
- **S2 — Repository documented:** repository documentation identifies the capability, but the exact public symbol was not extracted.
- **S3 — Architecture baseline:** relationship is established by architecture/audit material, not by exact API extraction.
- **S4 — Open:** requires further source inspection.

## 1. Yasin-Core

### Repository

`yusi20006-max/Yasin-core`

### Version identified in README

`3.3.0`

### Source-documented public areas

The repository README identifies these major public/API areas:

```text
agents
api
compatibility
config
context
core
di
events
execution
memory
observability
plugins
providers
runtime
sdk
security
storage
```

It explicitly describes `yasin_core/sdk/` as containing public SDK clients, interfaces, models, and compatibility helpers.

### Current evidence

| Surface | Evidence | Status |
|---|---|---|
| Runtime foundation | README + repository structure | S2 |
| SDK package | README + repository structure | S2 |
| API gateway | README + repository structure | S2 |
| Agent primitives | README + repository structure | S2 |
| Memory abstractions | README + repository structure | S2 |
| Event bus | README + repository structure | S2 |
| Storage interfaces | README + repository structure | S2 |
| Security manager/policy | README + repository structure | S2 |

The current GitHub code-search connector did not return exact symbol matches for the candidate names previously used in planning. Therefore those names are **not promoted to source-verified public API symbols**.

### Contract consequence

`CORE-SDK` remains a confirmed architectural contract, but its exact symbol-level API remains **S4/Open** until source files under `yasin_core/sdk/` are individually inventoried.

## 2. Yasin-Agent

The ecosystem architecture confirms `Yasin-Agent → Yasin-Core` and identifies an Agent SDK consumed by operational tooling.

Exact public class/function inventory remains a source-audit task.

Status: **S3/S4**.

## 3. YasinHub

The architecture confirms Hub as the control and observability plane and identifies Core SDK and Agent SDK integration.

The operational contract includes lifecycle/diagnostic concepts such as:

```text
status
health
start
stop
restart
doctor
```

These are architectural/operational capabilities. Exact Python/CLI/API symbols and payloads require direct source extraction.

Status: **S3/S4**.

## 4. YasinCLI

The canonical architecture identifies YasinCLI as the unified user-facing orchestration layer and records adapter coverage for Core, Agent, Hub, and Relay.

The exact repository identity/API surface still requires confirmation in the GitHub audit.

Status: **S4/Open** for exact symbols.

## 5. YasinRelay

Relay exposes an `AIProcessor` abstraction according to the repository architecture baseline.

The contract is confirmed conceptually:

```text
Relay pipeline
    ↓
AIProcessor
    ↓
provider implementation
```

Exact method signatures, protocols, and concrete implementations remain to be extracted.

Status: **S3/S4**.

## 6. YasinFeed

Feed contains provider/publisher boundaries for its content-processing and publishing pipeline.

Exact interface names and payload schemas require source-level extraction.

Status: **S3/S4**.

## 7. YasinPress

Press contains an optional Cloudflare Workers AI integration in its application pipeline.

The architectural contract is confirmed, but provider request/response models require source verification.

Status: **S3/S4**.

## 8. Yasin-AI

Yasin-AI is documented as an independent AI platform with runtime, knowledge, memory, API/service, extensions, and observability capabilities.

A canonical cross-project API contract has not yet been established.

Status: **S3 for platform boundary; S4 for ecosystem contract**.

## 9. Contract Registry Update Rules

A symbol should only be added to the exact API registry when at least one of the following is available:

1. source file path + symbol name;
2. stable generated API documentation backed by source;
3. repository tests demonstrating the public interface;
4. an explicit ADR defining a contract that implementation must satisfy.

README-only claims should remain S2.

## 10. Next Source Audit Batch

To complete this phase efficiently, inspect these files/directories in order:

```text
Yasin-Core
  → yasin_core/sdk/
  → yasin_core/api/
  → yasin_core/runtime/

Yasin-Agent
  → public package exports
  → SDK/interface modules

YasinHub
  → CLI entrypoint
  → SDK/API modules
  → lifecycle controller

YasinCLI
  → adapter interfaces
  → command registry

YasinRelay
  → AIProcessor definition
  → publisher interfaces

YasinFeed
  → publisher/provider interfaces

YasinPress
  → AI/provider integration

Yasin-AI
  → public service/API boundary
```

## 11. Current Conclusion

The API & Contract Registry is architecturally established, but the ecosystem is **not yet at symbol-level contract completeness**.

This is intentional. The documentation now distinguishes:

```text
Architecture fact
      ≠
Repository documentation
      ≠
Source-verified API symbol
```

This distinction is mandatory for reliable AI-assisted development.

## Status

**Source-Level API Audit v1 — Batch 1 complete.**

Exact public API extraction remains the next audit batch and should be performed project-by-project rather than inferred from names.
