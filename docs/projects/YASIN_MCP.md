# Yasin-MCP

## Evidence Status

**CONFIRMED — implemented and verified through Phase 1.**

Repository: `yusi20006-max/Yasin-MCP`

Phase 0 and Phase 1 are complete. The repository is intentionally **frozen at the Phase 1 read-only baseline** while the wider Yasin ecosystem is being audited and stabilized.

> Historical note: before implementation, YASIN-DOCS contained no documented Yasin-MCP architecture or contract. The implementation was therefore derived from the approved Yasin-MCP Issues #1–#10 and repository-level verification, rather than treating an undocumented target as an existing runtime contract.

## Role

Yasin-MCP is a standalone MCP access and integration layer for AI/Agent clients.

It provides a bounded, read-only interface to approved Yasin ecosystem information and integrations.

It does **not** replace:

- YASIN-DOCS
- Yasin-Core
- Yasin-Agent
- Yasin-AI
- YasinHub
- YasinCLI
- Yasin-Operations

It also does not make those projects depend on Yasin-MCP.

## Phase 1 Capabilities

The Phase 1 baseline establishes boundaries for:

- MCP server/runtime and transport
- versioned capability contracts
- capability discovery
- structured errors
- deny-by-default security policy
- safe configuration and secret handling
- structured logging and correlation identifiers
- YASIN-DOCS read-only access
- GitHub read-only inspection
- Yasin project registry/metadata
- read-only diagnostics and health inspection
- integration, contract, and security testing

## Read-Only Boundary

Phase 1 explicitly does not expose:

- arbitrary shell/process execution
- repository mutation
- issue/PR mutation
- merge/push/delete operations
- deployment
- start/stop/restart operations
- memory mutation
- secret retrieval
- arbitrary external API passthrough

## Evidence Model

Implementation claims must be supported by repository files, executed verification, or other explicit source evidence.

Documented target architecture must not be presented as proof of runtime implementation.

Where applicable, information should distinguish:

- `CONFIRMED`
- `TARGET`
- `PROPOSED`
- `UNRESOLVED`

## Freeze Policy

Yasin-MCP is currently frozen at Phase 1.

Allowed during the freeze:

- bug fixes
- security fixes
- documentation corrections
- compatibility fixes required by ecosystem changes

Not allowed without a new Phase 2 decision:

- new functional capability
- mutation tools
- new cross-project runtime coupling
- expansion of the MCP control surface

The freeze is recorded in Yasin-MCP Issue #23.

## Current Use

During the freeze, Yasin-MCP may be used as a read-only AI/agent access layer while the other Yasin projects are tested and stabilized.

## Phase 2

Phase 2 is intentionally not started.

It should be designed only after stable contracts and real integration requirements have been established by the wider ecosystem audit.
