# YASIN-DOCS

## Yasin Ecosystem Documentation Hub

YASIN-DOCS is the **canonical documentation and architecture repository for the Yasin Ecosystem**.

Its purpose is to give human developers and AI coding agents a single, structured entry point for understanding project roles, boundaries, dependencies, contracts, operations, and architectural decisions before changing code.

## Start Here

1. **[Canonical Ecosystem Architecture](docs/architecture/YASIN_ECOSYSTEM_CANONICAL_ARCHITECTURE_V1.md)** — read this first.
2. **[Dependency Matrix](docs/architecture/ECOSYSTEM_DEPENDENCY_MATRIX_V1.md)** — understand confirmed and unconfirmed project relationships.
3. **Project architecture documents** — read the document for the project being modified.
4. **ADRs** — read relevant decisions before changing cross-project boundaries.

## Canonical Architecture

```text
                         USER / OPERATOR
                                │
                                ▼
                           YasinCLI
                    Unified User Interface
                                │
                                ▼
                           YasinHub
                   Control + Observability
                                │
             ┌──────────────────┼──────────────────┐
             ▼                  ▼                  ▼
         Yasin-Core        Yasin-Agent       Applications
                                                │
                                      ┌─────────┼─────────┐
                                      ▼         ▼         ▼
                                   Relay      Feed      Press

                            Yasin-AI
                     Independent AI Platform
```

## Repository Map

| Repository | Role |
|---|---|
| `Yasin-Core` | Runtime and SDK foundation |
| `Yasin-Agent` | Agent/workflow execution |
| `Yasin-AI` | AI platform: runtime, knowledge, memory, API, extensions, observability |
| `YasinHub` | Ecosystem control and observability plane |
| `YasinCLI` | Unified user-facing CLI and ecosystem orchestration |
| `YasinRelay` | Telegram/content relay and publishing pipeline |
| `YasinFeed` | General content aggregation/processing/publishing |
| `YasinPress` | Specialized Persian-news publishing |
| `YASIN-DOCS` | Canonical ecosystem documentation |

## Documentation Structure

```text
YASIN-DOCS/
├── README.md
├── docs/
│   ├── architecture/
│   │   ├── YASIN_ECOSYSTEM_CANONICAL_ARCHITECTURE_V1.md
│   │   ├── ECOSYSTEM_DEPENDENCY_MATRIX_V1.md
│   │   ├── YASIN_RELAY_ARCHITECTURE.md
│   │   └── YASIN_FEED_PRESS_ARCHITECTURE.md
│   ├── adr/
│   │   └── Architecture decisions and audit records
│   ├── api/
│   │   └── Public APIs and integration contracts
│   ├── operations/
│   │   └── Runbooks and lifecycle procedures
│   └── compatibility/
│       └── Version and compatibility matrices
└── .github/
```

The existing top-level documents (`ARCHITECTURE.md`, `ECOSYSTEM.md`, `PROJECTS.md`, `ROADMAP.md`, etc.) remain valid historical/documentation entry points. The canonical architecture document is now the authoritative system-level baseline.

## Evidence Policy

YASIN-DOCS uses four evidence states:

- **Confirmed** — supported by repository/source evidence.
- **Inferred** — strongly indicated but not fully established.
- **Proposed** — future architecture or design option.
- **Unresolved** — requires further investigation or an ADR.

Never convert an inferred or proposed relationship into a confirmed dependency without evidence.

## Change Governance

Cross-project architectural changes should update:

1. the affected project architecture document;
2. the canonical architecture when the ecosystem graph changes;
3. the dependency matrix when dependencies change;
4. an ADR when the change is an intentional architectural decision;
5. API/compatibility documentation when public contracts change.

Individual repositories remain the source of truth for implementation. YASIN-DOCS is the source of truth for **system-level architecture and documented decisions**.

## AI Coding Agent Workflow

Before coding:

```text
Read YASIN-DOCS README
        ↓
Read Canonical Architecture
        ↓
Read Dependency Matrix
        ↓
Read target project architecture
        ↓
Inspect repository source + tests
        ↓
Classify the requested change
        ↓
Implement inside the correct boundary
        ↓
Run validation/tests
        ↓
Update YASIN-DOCS + ADR if architecture changed
```

The canonical architecture contains explicit rules for AI agents. Do not rely on repository names, assumptions, or stale conversation context to infer system relationships.

## What Belongs Here

- Ecosystem architecture
- Project responsibilities and boundaries
- Cross-project dependencies
- Data, control, AI, agent, and integration flows
- Public interfaces and architectural contracts
- ADRs
- Development and operational guidance
- AI-agent context and handoff documentation
- Ecosystem roadmap and project status
- Compatibility and release information

## What Does Not Belong Here

YASIN-DOCS is **not** the implementation repository for Yasin runtime or application code. Source code remains in each project's repository.

## Status

**YASIN-DOCS v1 documentation baseline established.**

The architecture is intentionally conservative: current facts are separated from future design decisions so this repository can serve as a reliable context package for both humans and AI coding agents.
