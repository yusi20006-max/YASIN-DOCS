# Yasin-MCP ↔ Yasin-Operations ↔ Hermes

**Status:** CONFIRMED architecture record  
**Date:** 2026-08-20  
**Scope:** Yasin-MCP, Yasin-Operations, Hermes integration boundary

## 1. Canonical architecture

`Yasin-MCP` is the MCP server / AI access layer for the Yasin ecosystem. `Yasin-Operations` is an independently deployable Operations component and is **not** itself an MCP server.

The intended integration path is:

```text
Hermes / other MCP client
        │
        │ MCP
        ▼
   Yasin-MCP
        │
        │ read-only Operations adapter
        │ subprocess: yasin-operations gateway
        │ JSONL stdin/stdout
        ▼
Yasin-Operations
        │
        ▼
Hermes-facing typed adapter → Core Executor
```

Therefore, Hermes should connect to **Yasin-MCP**, not directly register `Yasin-Operations` as an MCP server.

## 2. Yasin-MCP current implementation

Repository: `yusi20006-max/Yasin-MCP`

Verified repository description: standalone MCP server and AI access layer for the Yasin ecosystem.

The repository README currently states that the project is in the bootstrap phase and that the MCP server runtime itself is not yet present in that repository snapshot. It also defines the package layout for the future server, protocol, capabilities, tools, resources, adapters, policies, errors, audit, and configuration layers.

The repository defines an explicit read-only Phase-1 boundary: no repository mutation, deployment, lifecycle mutation, memory mutation, or arbitrary command execution. Existing Yasin projects must not become dependent on Yasin-MCP.

Evidence model:

- `CONFIRMED`: directly observed from an authoritative repository/runtime source.
- `TARGET`: documented architecture or intended behavior not yet live-verified.
- `PROPOSED`: future design suggestion.
- `UNRESOLVED`: not established.

## 3. Yasin-Operations current implementation

Repository: `yusi20006-max/Yasin-Operations`

Yasin-Operations currently provides:

- Operations Core / Executor boundary.
- Safety policy and typed operation contracts.
- CLI lifecycle/status/health/diagnostics surfaces.
- Optional Hermes-facing typed adapter.
- A local JSONL gateway over stdin/stdout.

It does **not** provide an MCP server, MCP discovery surface, or MCP listener. Its JSONL gateway must not be described as MCP.

The current gateway schema is version `1` and is invoked as:

```text
yasin-operations gateway
```

The gateway accepts line-delimited JSON on stdin and emits line-delimited JSON on stdout.

## 4. Existing Yasin-MCP Operations adapter

Yasin-MCP already contains the intended adapter boundary for Operations. It deliberately does not import the `yasin_operations` Python package.

Instead it starts the installed console executable:

```text
yasin-operations gateway
```

and communicates with it using the existing JSONL contract.

The Operations adapter exposes four fixed, read-only MCP capabilities:

| MCP tool | Operations operation | Safety |
|---|---|---|
| `yasin_operations_list_services` | `list_services` | `read_only` |
| `yasin_operations_service_status` | `service_status` | `read_only` |
| `yasin_operations_health` | `health_check` | `read_only` |
| `yasin_operations_diagnostics` | `diagnostics` | `read_only` |

There is intentionally no generic `invoke` / `execute` / caller-supplied operation path. The adapter hardcodes the allowed operation set and always sends `safety_class: read_only`.

This creates two independent safety boundaries: Yasin-MCP restricts the exposed operation set, and Yasin-Operations independently validates the operation's declared safety class against its own capability contract.

## 5. Availability behavior

Yasin-MCP checks for the `yasin-operations` executable before registering the Operations capability set.

If the executable is unavailable:

- Yasin-MCP can still start.
- Operations capabilities are not advertised.
- Other MCP capabilities remain unaffected.

If the executable disappears after registration, the adapter reports a structured unavailable-dependency error rather than crashing the MCP server.

## 6. Hermes relationship

Hermes is an **MCP client** in this architecture.

The correct conceptual connection is:

```text
Hermes
  │
  │ MCP
  ▼
Yasin-MCP
  │
  │ Operations adapter
  ▼
Yasin-Operations
```

The following direct connection is **not** the target architecture:

```text
Hermes
  │
  │ MCP
  ▼
Yasin-Operations
```

That direct connection fails because Yasin-Operations intentionally has no MCP server implementation.

The observed Hermes test on 2026-08-20 attempted to register `yasin-operations` as an MCP server and failed because no MCP server exists there. This is expected under the current architecture and must not be recorded as a Yasin-Operations defect.

## 7. Verification performed on 2026-08-20

### Yasin-Operations direct health

The installed CLI returned:

```text
success: True
health.status: healthy
health.target: self:runtime
health.failure_reason: None
services.summary.health: healthy
services.summary.total: 0
```

The JSON form also returned `success: true` and `health.status: healthy`.

### Yasin-Operations JSONL gateway

Both the installed gateway entry point and the Python module entry point executed successfully and returned valid schema-version-1 JSON responses.

The first test request used an unsupported target representation and returned `unsupported_health_target`; this was a request-contract mismatch, not a gateway failure. The direct CLI health contract subsequently confirmed the canonical runtime target as `self:runtime`.

### Hermes direct MCP registration attempt

Attempting to register `yasin-operations` directly in Hermes produced a connection failure and no MCP server configuration. Repository inspection confirms that this is expected because Yasin-Operations has no MCP server implementation.

## 8. Required operational setup

For Hermes to see Operations tools through Yasin-MCP, the environment in which Hermes launches Yasin-MCP must have both executables available:

```text
yasin-mcp
yasin-operations
```

The expected client registration is therefore conceptually:

```text
Hermes → yasin-mcp
```

not:

```text
Hermes → yasin-operations
```

The exact Hermes command/configuration must be validated against the installed Hermes version during live integration testing; repository documentation alone is not sufficient evidence of a successful live connection.

## 9. Boundary rules

1. Yasin-MCP owns the MCP protocol boundary.
2. Yasin-Operations owns Operations execution, safety policy, and runtime control semantics.
3. Yasin-MCP must not import Yasin-Operations' private Python modules.
4. The existing Yasin-Operations JSONL gateway remains a valid internal/local integration boundary.
5. JSONL and MCP are separate protocols and must not be conflated.
6. Operations capabilities exposed through Yasin-MCP remain read-only unless a future explicit architecture decision changes the safety contract.
7. Hermes is an external MCP client; it is not a dependency of Yasin-Operations.
8. Yasin-Operations must remain independently usable without Hermes or Yasin-MCP.
9. Any future mutating MCP capability requires a separate architecture/security decision and dedicated tests.

## 10. Source-of-truth rule

This document is the YASIN-DOCS cross-project reconciliation record for the relationship between Yasin-MCP, Yasin-Operations, and Hermes.

Repository implementation remains authoritative for implementation details. YASIN-DOCS is authoritative for the ecosystem-level ownership and boundary described here.

When either repository changes its integration contract, this document must be updated in the same architectural reconciliation cycle.
