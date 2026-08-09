# Yasin Ecosystem — Source-Verified Architecture Addendum

**Date:** 2026-08-09  
**Phase:** 5 — Per-Project Architecture  
**Status:** Final evidence pass for Phase 5

This document records architecture facts that became clear from current repository manifests, merged pull requests, release work, and integration audits. It supersedes earlier assumptions where stronger evidence exists.

## 1. Yasin-Core is a Real Installable Foundation

Yasin-Core is not merely a source tree shared with `PYTHONPATH`. Its current packaging defines a real `yasin-core` Python distribution with dynamic versioning sourced from `yasin_core.version.VERSION`, Python `>=3.9`, runtime dependencies on `requests`, `python-dotenv`, and `PyYAML`, and optional `psutil` observability support. fileciteturn84file0

The repository's recent production work explicitly verified editable installation from a clean virtual environment and a full 303/303 test suite after packaging. This makes package installation part of the intended consumer contract.

## 2. Yasin-Core Public SDK is a Boundary

Yasin-Agent integration work explicitly states that Agent uses the public `yasin_core.sdk` exports and does not import Core internals or duplicate Core tool/plugin implementations. Agent's application-level memory/context/session features are implemented through the Core SDK boundary.

This establishes the following ownership rule:

```text
Yasin-Core
  owns shared foundation/runtime capabilities and public SDK contracts

Yasin-Agent
  owns agent-specific policy, definitions, sessions and agent behavior
  and consumes Core through the public SDK
```

## 3. Yasin-Agent Uses Core for Shared Capabilities

Current Agent integration evidence covers:

- Core client initialization;
- agent registration;
- task execution;
- context execution;
- memory access;
- tool discovery/registration/execution;
- plugin discovery/registration/execution;
- application-level memory/context/session management.

Agent release work also documents workflows, tools, plugins, memory, sessions, and SDK integration as stable v1.0 capabilities.

The current integration audit verified 44/44 Agent tests against real Core 3.3.0 after removing a stale hard-coded Core version assertion.

## 4. YasinHub is an Ecosystem Management/Integration Layer

Current Hub integration evidence shows that Hub:

- uses the Core SDK;
- validates Core compatibility using Core's own semver compatibility engine;
- registers YasinFeed as `yasinfeed`;
- activates YasinRelay as a production ecosystem service;
- exposes service status/health/diagnostic functionality;
- has a CLI launcher with `status`, `start`, `stop`, `restart`, and `doctor` capabilities;
- provides dashboard event/log functionality.

Hub's Core compatibility was verified against real Core 3.3.0 with 104/104 tests passing.

Therefore the earlier description of Hub as only a lightweight status registry is incomplete. The more accurate model is:

```text
YasinHub
  ├── ecosystem registry
  ├── service integration
  ├── health/status/compatibility
  ├── events/logs/dashboard
  ├── YasinFeed integration
  └── YasinRelay integration
```

Hub is still not equivalent to the entire runtime of every service; it manages/integrates them through explicit contracts.

## 5. YasinCLI is a Real Control Plane

The current YasinCLI history provides direct evidence of integration with four core ecosystem services:

```text
YasinCLI
  ├── Yasin-Core package contract
  ├── Yasin-Agent CLI contract
  ├── YasinHub CLI contract
  └── YasinRelay runtime contract
```

The integration model is adapter-based rather than assuming that every component is a daemon.

### Service modes

The documented runtime contract distinguishes:

- `library` — Yasin-Core;
- `oneshot` — Yasin-Agent and YasinHub;
- `daemon` — YasinRelay.

Capability-aware lifecycle behavior prevents unsupported start/stop/restart operations from being treated as universally available.

### Current control-plane capabilities

Evidence includes:

- service discovery;
- health;
- logs;
- version reporting;
- start/stop/restart where supported;
- dependency-aware ecosystem orchestration;
- ecosystem profiles;
- developer project scaffolding;
- machine-readable output;
- stable exit codes;
- automation result/error contracts.

The Phase 4.5 PR added deterministic machine-readable output and stable CLI exit codes with tests. The Phase 3.5 PR added dependency-aware orchestration and cycle detection.

### Architectural consequence

The Master Architecture should treat YasinCLI as a **control-plane client/orchestrator**, not merely a convenience shell wrapper.

## 6. YasinRelay has a Standalone Source of Truth

Yasin-Core historically contained a `yasinrelay*` package namespace in its packaging configuration. More importantly, a recent Core PR explicitly synchronized embedded relay modules from the standalone YasinRelay source of truth.

This means the architecture must distinguish:

```text
YasinRelay repository
    = standalone relay source of truth

Yasin-Core yasinrelay namespace
    = synchronized/embedded compatibility or integration surface
```

The exact long-term removal/consolidation policy remains an ADR candidate.

YasinRelay itself is a production pipeline with routing, transport, monitoring, plugin interfaces, AI processing hooks, media handling, delivery status, retries, duplicate detection, and local task/session/conversation memory.

## 7. YasinRelay Has an Active Security Boundary

Current Relay history contains controlled Git-history secret cleanup work because a historical `.env` file and credential material had previously existed in repository history. The token was reported as revoked/rotated, and the cleanup process was designed to be gated, redacted, backed up, and prevented from force-pushing `main` automatically.

An open documentation PR remains around the final execution-state record.

This is operational security context that future agents must read before modifying Relay history or security workflows.

## 8. Yasin-AI is a Modular Production Platform

Current package metadata exposes these package domains:

```text
 yasinai*
 security_platform*
 developer_platform*
 knowledge_platform*
 api_service*
 observability*
```

It has a Python CLI entry point and test/coverage configuration. Current release work identifies v1.1.0 as the production documentation baseline.

Recent implementation history establishes:

- durable SQLite-backed long-term memory;
- durable SQLite-backed semantic knowledge retrieval;
- developer plugin SDK;
- transport-neutral API service layer;
- observability primitives;
- production deployment baseline;
- non-root container execution;
- read-only production filesystem/capability restrictions;
- dependency vulnerability auditing;
- release and maintenance policy.

The project still explicitly documents trusted-plugin and environment-specific boundaries; it should not be described as a formally certified security platform.

## 9. YasinFeed and YasinHub Have a Verified Integration

Hub's integration work registers `yasinfeed` in its service registry and provides launch/monitoring behavior. Feed service/repository failure paths were hardened and integration tests were added.

Therefore:

```text
YasinHub
   │ manages/integrates
   ▼
YasinFeed
```

is now a source/history-verified relationship rather than a conceptual arrow.

## 10. YasinFeed and YasinPress Remain Distinct Applications

Both process content/news, but no evidence gathered in this phase justifies collapsing them into one service.

The architecture should preserve separate ownership until a direct contract or duplication-removal decision is made.

## 11. FeedBridge is Not an OpenFeed Runtime Dependency

FeedBridge vendors its fetcher and invokes it locally. Its relationship with OpenFeed is best described as lineage/reuse rather than a requirement to run an OpenFeed service.

## 12. TJC is Development Infrastructure

TJC remains a Jules automation/workflow tool. It belongs in the development/tooling layer and should not be treated as a runtime dependency of Core, Agent, Hub, Relay, Feed, or Press without explicit evidence.

## 13. Phase-5 Evidence Confidence

### High confidence

- Core is the foundation and has a public SDK/package boundary.
- Agent consumes Core public SDK capabilities.
- Hub integrates Core, Feed, and Relay.
- CLI integrates Core, Agent, Hub, and Relay through explicit runtime contracts.
- Relay is a standalone source of truth for relay functionality.
- AI is a modular platform with explicit package domains and production hardening.
- FeedBridge's fetcher is locally vendored.

### Medium confidence

- Exact module-level import graphs across all repositories.
- Exact persistence schemas and migrations.
- Complete runtime call graphs.
- Full cross-project configuration key ownership.
- Complete CI/CD topology for every repository.

### Not yet verified

- Full source tree graph for every repository.
- Every public symbol and stable API signature.
- Every deployment environment.
- Every producer/consumer relationship.
- Complete issue/PR/release history for every supporting/candidate repository.

## 14. Phase-5 Closure Rule

Phase 5 is considered complete at the **architecture-documentation level** when every discovered project has a scoped record and all high-confidence cross-project contracts discovered during the audit are documented.

Unverified low-level facts are not fabricated. They are explicitly carried forward as evidence gaps for Phase 6 and later audits.
