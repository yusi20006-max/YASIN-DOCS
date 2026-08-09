# Verified Cross-Project Contract Evidence

**Phase:** 5 — Source-Level Audit  
**Status:** Initial verified-evidence register

This file contains only relationships for which the current repository evidence is strong enough to document a concrete contract or implementation relationship. It does not attempt to be the final dependency graph.

## 1. Yasin-Agent ↔ Yasin-Core

Repository documentation provides evidence that Yasin-Agent has a `YasinCoreAgentAdapter` and integrates with the Yasin-Core SDK. This establishes an implementation/documented integration boundary.

**Current status:** Verified integration exists; exact API surface still requires source audit.

## 2. FeedBridge ↔ Vendored Fetcher

FeedBridge documents a fetcher executable located inside its own repository. The Fetch Engine invokes it and consumes JSON from stdout.

**Current status:** Verified local subprocess contract.

## 3. FeedBridge ↔ OpenFeed

The relationship is currently documented as lineage/reuse rather than a runtime service dependency. The fetcher is vendored into FeedBridge.

**Current status:** Verified non-service reuse evidence; exact historical lineage should not be confused with runtime dependency.

## 4. YasinCLI ↔ Its Local Runtime

`package.json` defines `src/index.js` as the Node package entry point and `yasin.sh` as the CLI executable. Tests include Jest, ESLint, and a smoke test.

**Current status:** Verified local packaging/CLI contract.

## 5. Yasin-AI ↔ CLI Entry Point

`pyproject.toml` defines the executable `yasin` entry point as `yasinai.cli.security_entrypoint:main`.

**Current status:** Verified package-level CLI entry point.

## 6. Yasin-Core ↔ Package Boundary

`pyproject.toml` identifies Yasin-Core as the kernel/runtime foundation and explicitly includes `yasin_core*` and `yasinrelay*` in package discovery.

**Current status:** Verified packaging fact. The architectural meaning of the `yasinrelay*` namespace remains an investigation item.

## Contract Verification Rules

A relationship is not promoted to this file merely because:

- two repositories have similar names;
- one project mentions another in a roadmap;
- a future architecture diagram contains an arrow;
- the projects solve related problems.

Source, configuration, package metadata, executable invocation, or a documented implementation-backed contract is required.

## Next Verification Targets

- Yasin-Core public SDK imports and entry points;
- Yasin-Agent adapter implementation and consumed Core symbols;
- YasinCLI integration mechanism for Yasin projects;
- YasinHub API and actual consumers;
- YasinFeed/YasinPress shared or duplicated capabilities;
- YasinRelay/OpenFeed/FeedBridge actual transport boundaries;
- storage and configuration contracts across all services.
