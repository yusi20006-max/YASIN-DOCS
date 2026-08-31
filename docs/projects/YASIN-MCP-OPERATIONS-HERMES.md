# Yasin Core Stack ↔ Operator Stack Architecture

**Status:** CONFIRMED ecosystem architecture record  
**Date:** 2026-08-30  
**Scope:** YasinHub, Yasin-Agent, Yasin-Core, Yasin-MCP, Yasin-Operations, Hermes, Telegram

## 1. Purpose

Yasin has two complementary architectural paths with different responsibilities. They must remain separate.

The **Yasin Core Stack** is the original application/runtime architecture and must continue to operate normally and independently.

The **Operator Stack** is an additional integration layer introduced for reporting, monitoring, diagnostics, and extra control through Telegram and Hermes. It must not replace, restructure, or become a runtime dependency of the Core Stack.

This separation is an architectural boundary, not merely an implementation preference.

## 2. Yasin Core Stack — original architecture

The original Yasin architecture remains:

```text
                 YasinHub
               Control Plane
                    │
                    ▼
               Yasin-Agent
               Agent Runtime
                    │
                    ▼
                Yasin-Core
          Core / Memory / State
                    │
             ┌──────┴──────┐
             ▼             ▼
        YasinRelay     other core
                       Yasin components
```

This path represents the normal Yasin application/runtime flow.

### Core-stack rules

- YasinHub remains the primary Control Plane for the Yasin ecosystem.
- Yasin-Agent remains the primary Agent Runtime.
- Yasin-Core remains the core foundation for shared core functionality, memory, state, and related runtime concerns.
- Existing Yasin components continue to communicate through their established contracts.
- The Core Stack must be usable without Hermes.
- The Core Stack must be usable without Yasin-MCP.
- The Core Stack must be usable without Yasin-Operations.
- Adding the Operator Stack must not force changes to the normal Core Stack execution path unless an explicit future architecture decision says otherwise.

## 3. Operator Stack — additional architecture

The newer operator/reporting architecture is:

```text
                    Telegram
                       │
                       ▼
                    Hermes
                 Operator Client
                       │
                       │ MCP
                       ▼
                  Yasin-MCP
              MCP / AI Access Layer
                       │
                       │ read-only Operations adapter
                       │ JSONL
                       ▼
              Yasin-Operations
          Operations / Monitoring Layer
```

Its purpose is to provide an additional operator-facing interface for:

- Telegram-based reporting.
- Monitoring and diagnostics.
- Health/status visibility.
- Extra operational control through explicitly exposed capabilities.
- Hermes-based interaction with the Yasin ecosystem.

The Operator Stack is therefore an **overlay/integration layer**, not a replacement for the original Yasin architecture.

## 4. Exact ownership of the boundaries

### YasinHub

Owns the primary Yasin Control Plane and the normal management/orchestration surface of the Core Stack.

### Yasin-Agent

Owns the primary Agent Runtime. It remains the normal execution environment for Yasin agents.

### Yasin-Core

Owns the core shared runtime/foundation responsibilities, including the established memory/state architecture and core contracts.

### Yasin-MCP

Owns the **MCP protocol boundary** for external AI/agent clients such as Hermes.

Yasin-MCP is the controlled gateway through which an MCP client can access explicitly exposed Yasin capabilities.

### Yasin-Operations

Owns the **Operations boundary**: operational execution semantics, safety policy, typed operation contracts, diagnostics, and its existing JSONL gateway.

Yasin-Operations is independently usable and is **not an MCP server**.

### Hermes

Acts as an external/operator-side MCP client. Hermes is not part of the Core Stack and must not become a dependency of Yasin-Core, Yasin-Agent, YasinHub, or Yasin-Operations.

### Telegram

Is an operator-facing communication surface. It belongs to the Operator Stack and does not replace the YasinHub Control Plane.

## 5. Integration between the two stacks

The stacks may interact, but only through explicit boundaries:

```text
                 CORE STACK

       YasinHub → Yasin-Agent → Yasin-Core
            │
            │
            │ explicit controlled access
            ▼
       ┌─────────────────────────┐
       │      OPERATOR STACK     │
       │                         │
       │ Telegram → Hermes       │
       │              │          │
       │              ▼ MCP      │
       │          Yasin-MCP      │
       │              │          │
       │              ▼ JSONL    │
       │      Yasin-Operations   │
       └─────────────────────────┘
```

The existence of the Operator Stack does **not** mean that the Core Stack has been replaced by MCP, Hermes, or Operations.

## 6. What must NOT happen

The following architectural mixing is explicitly prohibited unless a future architecture decision changes it:

```text
❌ Hermes → Yasin-Agent as a replacement runtime path
❌ Hermes → Yasin-Core directly
❌ Hermes → Yasin-Operations as an MCP server
❌ Yasin-Core → Hermes dependency
❌ Yasin-Agent → Hermes dependency
❌ YasinHub → Hermes dependency for normal operation
❌ Core Stack → Yasin-MCP hard dependency
❌ Core Stack → Yasin-Operations hard dependency
❌ Treating JSONL as MCP
❌ Treating Yasin-Operations as an MCP server
❌ Moving normal agent execution from Yasin-Agent into Hermes
```

In particular, Hermes must not become the new Agent Runtime, and Yasin-MCP must not become the new Core Runtime.

## 7. Failure isolation

The two stacks must fail independently as much as practical.

If Hermes is unavailable, the normal Yasin Core Stack must continue to work.

If Telegram is unavailable, the normal Yasin Core Stack must continue to work.

If Yasin-MCP is unavailable, the normal Yasin Core Stack must continue to work.

If Yasin-Operations is unavailable, Yasin-MCP may hide or disable the Operations capability set while preserving other capabilities; the Core Stack must remain unaffected.

This principle prevents monitoring/operator integrations from becoming single points of failure for the main Yasin runtime.

## 8. Security and capability boundary

The Operator Stack must expose only explicitly defined capabilities.

The current Yasin-MCP ↔ Yasin-Operations integration is intentionally read-only at the Operations boundary. The adapter exposes fixed operations rather than a generic caller-supplied execution mechanism.

A future mutating capability requires a separate architecture/security decision, explicit operation contract, safety classification, and dedicated verification.

The Operator Stack must not provide an unrestricted shell, arbitrary process execution, arbitrary repository mutation, or an unbounded `execute_operation` mechanism merely because Hermes is connected.

## 9. Protocol boundaries

The protocols have distinct ownership:

```text
Hermes
  │
  │ MCP
  ▼
Yasin-MCP
  │
  │ JSONL gateway
  ▼
Yasin-Operations
```

MCP and JSONL are separate protocols.

Yasin-MCP translates the external MCP interaction into the explicitly supported Operations interface. Yasin-Operations continues to own and validate its own operation contract.

## 10. Architectural principle

The guiding principle is:

> **The Operator Stack observes and controls the Yasin Core Stack through explicit boundaries; it does not become the Yasin Core Stack.**

Therefore:

```text
Original Yasin architecture
        = Core Stack
        = normal production/runtime path

New Hermes/MCP/Operations architecture
        = Operator Stack
        = additive reporting/monitoring/control path
```

Both can coexist. They solve different problems and should evolve independently.

## 11. Source-of-truth rule

This document is the ecosystem-level architectural record for the separation between the original Yasin Core Stack and the newer Hermes/MCP/Operations Operator Stack.

Implementation details remain authoritative in the individual repositories:

- `yusi20006-max/YasinHub`
- `yusi20006-max/Yasin-Agent`
- `yusi20006-max/Yasin-core`
- `yusi20006-max/Yasin-MCP`
- `yusi20006-max/Yasin-Operations`

When an implementation changes an integration boundary, this architecture record must be reconciled so that the two-stack separation remains explicit.

## 12. Existing Yasin-MCP ↔ Yasin-Operations reconciliation

The previous integration record remains valid: Yasin-MCP owns MCP, Yasin-Operations owns Operations, and Yasin-Operations is not itself an MCP server. Hermes therefore connects to Yasin-MCP rather than registering Yasin-Operations directly as an MCP server.

The existing detailed reconciliation and verification history is preserved in the repository's project documentation and should be read together with this ecosystem-level architecture record.
