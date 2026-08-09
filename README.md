# YASIN-DOCS

## Yasin Ecosystem Documentation Hub

YASIN-DOCS is the central documentation and architectural knowledge repository for the **Yasin Ecosystem**.

Its purpose is to provide a single, structured source of truth for understanding how the Yasin projects fit together, what each project is responsible for, how they communicate, and how developers and AI coding agents should work across the ecosystem.

## What belongs here

- Ecosystem architecture
- Project responsibilities and boundaries
- Cross-project dependencies
- Data, control, AI, agent, and integration flows
- Public interfaces and architectural contracts
- Architecture Decision Records (ADRs)
- Development and operational guidance
- AI-agent context and project handoff documentation
- Ecosystem roadmap and project status

## What does not belong here

YASIN-DOCS is **not** the implementation repository for the Yasin runtime or application projects. Source code remains in its respective repository. This repository documents the system-level relationships, contracts, decisions, and knowledge needed to work safely across those repositories.

## Documentation Structure

```text
YASIN-DOCS/
├── README.md
├── ARCHITECTURE.md
├── ECOSYSTEM.md
├── PROJECTS.md
├── ROADMAP.md
├── CONTRIBUTING.md
├── DEVELOPMENT.md
├── SECURITY.md
│
├── docs/
│   ├── architecture/
│   ├── projects/
│   ├── development/
│   ├── operations/
│   └── ai/
│
└── .github/
```

## Core Principle

> **YASIN-DOCS is the system-level source of truth; individual repositories remain the source of truth for their own implementation.**

Documentation must distinguish between:

- current implementation
- intended architecture
- planned roadmap
- experimental or provisional behavior

No architectural fact should be presented as implemented merely because it is planned.

## AI / Coding Agent Use

This repository is designed to be consumed by AI coding agents as well as human developers. The documentation will therefore explicitly describe:

1. what each project is;
2. what it is not;
3. its responsibilities and boundaries;
4. its dependencies and consumers;
5. its public interfaces;
6. its current implementation status;
7. its known constraints and decisions; and
8. the correct procedure for making cross-project changes.

## Project Status

YASIN-DOCS is being established in phases. The initial phase creates the documentation foundation. Later phases will audit the actual Yasin repositories and replace assumptions with verified repository facts.
