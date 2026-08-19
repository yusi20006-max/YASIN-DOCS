# Yasin-MCP Project Architecture

## Status

**Target / implementation planned** — see ADR-0013.

## Repository

`yusi20006-max/Yasin-MCP`

## Mission

Provide a standalone MCP server that gives AI agents a safe, versioned, evidence-aware interface to the Yasin ecosystem.

## Responsibility

Yasin-MCP owns:

- MCP protocol exposure;
- capability discovery;
- bounded tools/resources;
- integration adapters;
- stable machine-readable error contracts;
- future AI-facing authorization/safety boundaries.

Yasin-MCP does not own:

- Yasin-AI model/provider infrastructure;
- Yasin-Core runtime internals;
- Yasin-Agent workflow semantics;
- YasinHub control-plane logic;
- YasinCLI command semantics;
- Yasin-Operations operational authority;
- application business logic;
- ecosystem architecture documentation.

## Primary Consumers

Potential consumers include:

- ChatGPT;
- coding agents;
- Yasin-Agent and future agent clients;
- operator/analysis tooling that supports MCP.

Consumption is optional. No existing Yasin runtime becomes dependent on Yasin-MCP merely by using the interface.

## Initial Sources

1. YASIN-DOCS — architecture, ADRs, specifications and project metadata.
2. GitHub — repositories, issues, PRs and CI/status information through a bounded adapter.
3. Public Yasin APIs/contracts — project state and capabilities.
4. Yasin-Operations — optional operational information through a public adapter.

## Initial Safety Posture

Phase 1 is read-only.

No arbitrary shell execution, repository mutation, deployment, lifecycle mutation, or memory deletion is exposed in the initial release.

## Success Criteria

Yasin-MCP is considered ready to leave Phase 1 when:

- the server starts cleanly in a fresh environment;
- capability discovery is deterministic;
- tool/resource contracts are typed and versioned;
- Docs and GitHub read paths work without private imports;
- unavailable adapters fail gracefully;
- tests and CI are green;
- security checks pass;
- documentation matches implementation;
- no existing Yasin project has gained a mandatory dependency on Yasin-MCP.

## Related Architecture

- `docs/architecture/YASIN_MCP_ARCHITECTURE_V1.md`
- `docs/adr/ADR-0013-yasin-mcp-ai-access-layer.md`
- `docs/architecture/YASIN_ECOSYSTEM_CANONICAL_ARCHITECTURE_V1.md`
- `docs/architecture/ECOSYSTEM_DEPENDENCY_MATRIX_V1.md`
