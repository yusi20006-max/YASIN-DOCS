# Yasin Ecosystem

## Overview

The Yasin Ecosystem is a collection of related repositories that together provide foundation/runtime capabilities, agent capabilities, AI services, management and orchestration, integration, content pipelines, applications, developer tooling, and centralized documentation.

The exact role and current status of every project will be verified during the repository-discovery phase. This document is intentionally a high-level overview and must not replace repository-specific audits.

## Architectural Principle

Each project should have a clear primary responsibility and a defined boundary. Functionality should be implemented in the layer that owns that responsibility rather than duplicated across repositories for convenience.

## Conceptual Layers

```text
Users / Developers
        |
        v
Control Plane / Management
        |
        +-------------------+
        |                   |
        v                   v
Agent / Runtime        Domain Applications
        |                   |
        v                   v
Foundation            Content / Integration
        |
        +-------------------+
                    |
                    v
                AI Services
```

This is a conceptual model only. The verified architecture will be derived from the actual repositories and their current interfaces.

## System Boundaries

The ecosystem documentation distinguishes at least these concerns:

- foundation and runtime;
- agents and execution;
- AI service/provider abstraction;
- management and orchestration;
- integration and relay;
- content ingestion and publishing;
- domain applications;
- control-plane tooling;
- documentation;
- developer and infrastructure tooling.

## Source of Truth

- Individual repositories are authoritative for implementation details.
- YASIN-DOCS is authoritative for cross-project architecture, documented boundaries, decisions, and ecosystem-level guidance.
- When documentation and implementation disagree, the discrepancy must be recorded and resolved rather than silently assuming one is correct.
