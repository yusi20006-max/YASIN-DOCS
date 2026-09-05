# Yasin Ecosystem Architecture

This document is the top-level architecture entry point for the Yasin ecosystem.

## Current canonical runtime model

```text
User / Operator
      │
      ▼
YasinCLI / approved operator clients
      │
      ▼
YasinHub — Control Plane + Observability
      │
      ├── lifecycle / PID authority
      ├── health / status
      └── PWA control surface
      │
      ├──────────────┬───────────────┐
      ▼              ▼               ▼
Yasin-Core     Yasin-Agent      Domain services
                  │             Relay / Feed / Press
                  │               │
                  └──────┬────────┘
                         ▼
                    Yasin-AI
               Canonical AI Plane
```

### Non-negotiable boundaries

- **YasinHub is the sole ecosystem lifecycle/PID authority.** Clients and the PWA request lifecycle operations; they do not maintain an independent authoritative process state.
- **Yasin-Agent owns agent/workflow execution.** It does not become a second Control Plane.
- **YasinRelay owns content relay/fetch/process/publish semantics.**
- **Yasin-AI owns shared AI capability/provider boundaries.** Consumers use explicit public contracts and must not depend on private implementation modules.
- **Yasin-MCP owns the MCP protocol boundary.** It is not a second lifecycle authority.
- **Yasin-Operations is an optional operations provider/gateway and does not replace YasinHub as Control Plane.**

## Evidence status — 2026-09-05

The final YasinHub ecosystem acceptance track (#174) verified the software/runtime baseline on Android 11 API 30 ARM64 Termux. Current verified test totals are:

| Component | Result |
|---|---:|
| YasinHub | 478 passed |
| Yasin-Agent | 240 passed |
| YasinRelay | 108 passed |
| Yasin-AI | 415 passed |

The YasinHub acceptance also verified real child-process lifecycle behavior, PID identity/termination handling, PWA backend/API authority, and security regressions.

The acceptance is **PARTIAL, not FULL PASS** because two external acceptance items remain: valid operator publishing configuration is required for a real publish E2E, and visual PWA acceptance requires an actual browser/mobile viewport. These are explicitly tracked rather than represented as successful.

## Architecture governance rule

YASIN-DOCS is authoritative for cross-project architecture, boundaries, terminology, and decisions. Individual repositories remain authoritative for implementation. Any discrepancy must be recorded and reconciled with evidence.

## Related documents

- [Ecosystem](ECOSYSTEM.md)
- [Project Registry](PROJECTS.md)
- [Roadmap](ROADMAP.md)
- [Development Guide](DEVELOPMENT.md)
- [Canonical architecture](docs/architecture/YASIN_ECOSYSTEM_CANONICAL_ARCHITECTURE_V1.md)
- [Termux compatibility contract](docs/compatibility/TERMUX_FIRST_COMPATIBILITY_CONTRACT_V1.md)
