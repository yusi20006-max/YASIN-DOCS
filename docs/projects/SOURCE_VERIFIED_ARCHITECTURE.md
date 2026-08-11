# Yasin Ecosystem — Source-Verified Architecture Addendum

**Date:** 2026-08-09  
**Phase:** 5 — Per-Project Architecture  
**Status:** Final evidence pass for Phase 5

This document records architecture facts that became clear from current repository manifests, merged pull requests, release work, and integration audits. It supersedes earlier assumptions where stronger evidence exists.

## 1. Yasin-Core is a Real Installable Foundation

Yasin-Core is not merely a source tree shared with `PYTHONPATH`. Its current packaging defines a real `yasin-core` Python distribution with dynamic versioning sourced from `yasin_core.version.VERSION`, Python `>=3.9`, runtime dependencies on `requests`, `python-dotenv`, and `PyYAML`, and optional `psutil` observability support. fileciteturn84file0

> **Update (2026-08-09, later same day):** The 303/303 figure below is superseded. A follow-up structural cleanup removed a full byte-identical duplicate of the `yasinrelay/` package and the Go `fetcher/` source that had lived inside this repo (see section 6 update) along with the Core-side tests that covered that duplicate code. The suite is now **237/237**, and CI (GitHub Actions, Python 3.9 + 3.12) now runs it automatically on every push/PR -- Core previously had no CI at all.
>
> A separate security audit pass also found and fixed two real vulnerabilities in `yasin_core/security/`: a hardcoded backdoor API key (`"admin-key"` granted wildcard `api:*` access to anyone) and a weak default-key XOR "encryption" scheme in the credential protector (fixed with a counter-mode keystream + HMAC integrity check, no external crypto dependency added). Any prior claim of a security PASS audit predates these fixes and should not be trusted without re-verification.
>
> **Packaging is no longer Core-specific.** The same pyproject.toml treatment (dynamic version, real `pip install -e .`) has since been applied to **Yasin-agent**, **YasinHub**, and **YasinRelay** as well -- all three previously had zero packaging metadata, meaning none of them were actually pip-installable, which silently broke `yasin agent version` / `yasin hub version` / `yasin relay version` in YasinCLI (see section 5) in any real deployment. All four packages (Core, Agent, Hub, Relay) were verified together in one venv and confirmed to report correct live versions through the real CLI.

The repository's recent production work explicitly verified editable installation from a clean virtual environment and a full 303/303 test suite after packaging (superseded, see update above). This makes package installation part of the intended consumer contract.

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

> **Update (2026-08-09):** "Version reporting" above was not actually working for Core before a fix. `BaseEcosystemAdapter` accepted a `defaultVersionCommandArgs` constructor field but never stored or used it; the fallback logic that derives `versionCommandArgs` only produced a correct value when `versionCommand === command`, which is true for Agent/Hub/Relay (their version check reuses the same base command, just appending `--version`) but is never true for Core (`mode: 'library'`, no `command` at all, only a standalone `versionCommand`). This silently resolved to an empty args array, so `yasin core version` always returned `{ version: null, status: 'unknown' }` even against a fully working install. Fixed by storing and preferring the adapter's own `defaultVersionCommandArgs` in the fallback chain; verified live end-to-end against a real pip-installed Core 3.3.0 (now correctly returns `{ version: '3.3.0', status: 'ok' }`), with a regression test confirmed to fail on the pre-fix code.

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

## 6. YasinRelay has a Standalone Source of Truth (RESOLVED)

> **Update (2026-08-09):** This is resolved, not an open ADR candidate anymore. Verification found the embedded `yasinrelay/` package inside Yasin-Core was not a "synchronized" or evolving mirror -- it was a full, byte-identical copy (28 files, plus the Go `fetcher/` source) of code already living in the standalone YasinRelay repository, confirmed via `diff -rq` showing zero divergence. Yasin-Core's own `docs/architecture/DEPENDENCY_RULES.md` had an explicit "Core/Relay Exception" saying this duplication must not be removed until a formal migration was scheduled -- but that note assumed a *divergent* reimplementation scenario that didn't match reality (no divergence existed, so no behavioral migration was needed). The duplicate `yasinrelay/`, `fetcher/`, the Core-side tests that covered them, a stale duplicate `ARCHITECTURE.md`, and a plugin example that depended on the removed code were all deleted from Yasin-Core. Core's `pyproject.toml` no longer packages a `yasinrelay*` namespace. Yasin-Core's own architecture docs (DEPENDENCY_RULES.md, ECOSYSTEM_MAP.md, BOUNDARIES.md) were updated to record this as resolved.

Yasin-Core historically contained a `yasinrelay*` package namespace in its packaging configuration. More importantly, a recent Core PR explicitly synchronized embedded relay modules from the standalone YasinRelay source of truth.

This means the architecture must now be read as:

```text
YasinRelay repository
    = sole source of truth for relay functionality

Yasin-Core
    = no longer contains any yasinrelay/fetcher code (removed)
```

Separately, the standalone YasinRelay repository's own test suite had the same stale bugs found in the Core-side copy (a `Path.exists` mocking gap causing 5 false test failures, and a hardcoded assertion of an old Core SDK version) -- these had not been fixed on the canonical repo since they were previously only ever edited on the Core-side duplicate. Both were fixed directly on the standalone YasinRelay repository once it became the sole copy.

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
- Complete CI/CD topology for every repository. **Partial update (2026-08-09):** Core, Yasin-agent, YasinRelay, and Yasinfeed are confirmed to have GitHub Actions CI (Core's was added in this pass; it previously had none). YasinHub is confirmed to still have **no CI** at all.

### Not yet verified

- Full source tree graph for every repository.
- Every public symbol and stable API signature.
- Every deployment environment.
- Every producer/consumer relationship.
- Complete issue/PR/release history for every supporting/candidate repository.

## 14. Phase-5 Closure Rule

Phase 5 is considered complete at the **architecture-documentation level** when every discovered project has a scoped record and all high-confidence cross-project contracts discovered during the audit are documented.

Unverified low-level facts are not fabricated. They are explicitly carried forward as evidence gaps for Phase 6 and later audits.
