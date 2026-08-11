# Yasin-Core — Project Architecture Record

## Identity

- Repository: `yusi20006-max/Yasin-core`
- Default branch: `main`
- Public repository
- Current documented version: `3.3.0`
- Current state: release-freeze validation

## Responsibility

Yasin-Core is documented as the central runtime layer of the Yasin AI Ecosystem. It provides shared execution/runtime, context and memory, API/integration, compatibility, storage, security, observability, plugin/provider, SDK and lifecycle foundations.

## Module Map

```text
agents/          agent primitives, planning, runtime, tools, task models
api/             API gateway, auth, models, errors
compatibility/   adapters, migration, version coordination
config/          configuration schema/defaults
context/         context engine
core/            bootstrap, lifecycle, orchestrator, runtime foundations
di/              dependency injection
events/          event model/bus
execution/       execution engine, queues, workers, distributed execution, scheduler
memory/          in-memory/persistent memory abstractions
observability/   logging, metrics, performance, monitoring
plugins/         plugin contracts, bridge, registry
providers/       provider interfaces/adapters
runtime/         runtime interfaces/models/registry/service manager
sdk/             public SDK clients/interfaces/models
security/        audit/policy/protection/security manager
storage/         storage interfaces/implementations
```

## Ecosystem Position

The README explicitly identifies compatibility surfaces used by components such as YasinCLI, YasinHub, YasinRelay and agent-related tooling. Exact imports, API contracts and runtime dependency edges require source-level verification.

## Testing

The documented normal entry point is `pytest`. The repository states that tests cover runtime, agents, API, compatibility, execution, scheduler, storage, SDK, observability, security and integration behavior.

## Release / Risk Notes

Release-freeze priorities include documentation consistency, repository identity correction, audit/production validation, changelog/release-note alignment and final review before release tagging.

## Boundary

Other projects should consume stable Core contracts rather than independently duplicating runtime, memory, security, SDK or observability primitives unless an explicit architectural decision establishes a separate boundary.

## Audit Status

**Level 3:** role and module architecture are strongly documented. Public API surface, concrete dependency graph, consumers, configuration internals and CI details still require source-level audit.

> **Update (2026-08-09):** Several of these gaps are now closed. CI exists (GitHub Actions, Python 3.9 + 3.12, runs pytest on push/PR — previously there was none). Packaging is real (`pyproject.toml`, `pip install -e .` verified from a clean venv). The dependency graph with YasinHub, Yasin-agent, and YasinRelay has been live-verified (all three actually import and call real Core, not mocks, confirmed end-to-end through the real YasinCLI). A security audit found and fixed a hardcoded admin API-key backdoor and a weak XOR credential-encryption scheme — see `docs/projects/SOURCE_VERIFIED_ARCHITECTURE.md` §1 for full detail. Test suite is currently 237/237 (not the historical 289/303 figures found elsewhere in this repo, both of which predate a later structural cleanup that removed a duplicated `yasinrelay/` package from Core — see §6 of the same document).
