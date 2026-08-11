# Yasin Ecosystem Architecture

This document is the top-level entry point to the architecture documentation of the Yasin Ecosystem.

## Purpose

Yasin is a multi-repository software ecosystem rather than a single application. Its projects have distinct responsibilities and must be understood through their boundaries and relationships.

The architecture documentation therefore treats the ecosystem as a system of cooperating components while keeping implementation ownership inside each project's repository.

## Architecture Documentation

The detailed architecture is maintained under [`docs/architecture/`](docs/architecture/).

Project-specific production architecture and roadmaps are maintained under [`docs/projects/`](docs/projects/).

### YasinPress

- [YasinPress Architecture & Production Roadmap](docs/projects/yasinpress/ARCHITECTURE-ROADMAP.md)

This roadmap is the shared target architecture for the YasinPress news-ingestion, article-intelligence, AI, queue, publishing, monitoring, PWA, scheduler and recovery pipeline. It explicitly distinguishes repository-verified implementation from planned production behavior.

## Planned Architecture Coverage

The architecture documentation covers:

- ecosystem vision and boundaries;
- global component and layer model;
- project responsibility matrix;
- dependency relationships;
- data flow;
- control flow;
- AI flow;
- agent and memory architecture;
- integration and transport boundaries;
- configuration and security boundaries;
- deployment and observability;
- testing and compatibility;
- architecture decisions;
- project-specific production roadmaps.

## Current-State Rule

The architecture repository must distinguish verified implementation from proposed design. Repository audits are authoritative for current implementation details.

## Related Documents

- [Ecosystem Overview](ECOSYSTEM.md)
- [Project Registry](PROJECTS.md)
- [Roadmap](ROADMAP.md)
- [Development Guide](DEVELOPMENT.md)
- [AI Documentation](docs/ai/)
