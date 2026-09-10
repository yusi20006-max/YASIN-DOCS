# Yasin Ecosystem Architecture

This document is the top-level entry point to the architecture documentation of the Yasin Ecosystem.

## Purpose

Yasin is a multi-repository software ecosystem rather than a single application. Its projects have distinct responsibilities and must be understood through their boundaries and relationships.

The architecture documentation therefore treats the ecosystem as a system of cooperating components while keeping implementation ownership inside each project's repository.

## Architecture Documentation

The detailed architecture is maintained under [`docs/architecture/`](docs/architecture/).

Project-specific production architecture and roadmaps are maintained under [`docs/projects/`](docs/projects/).

### YasinCoder

- [YasinCoder Architecture & Production Roadmap](docs/projects/yasincoder/ARCHITECTURE-ROADMAP.md)
- [YasinCoder Phase 2 AI Integration Audit](docs/projects/yasincoder/PHASE2-AI-INTEGRATION-AUDIT.md)

YasinCoder is the canonical repository for the Yasin coding-agent application. Its local/cloud provider integration, coding workflows, project intelligence and web control plane should converge in that repository.

### YasinPress

- [YasinPress Architecture & Production Roadmap](docs/projects/yasinpress/ARCHITECTURE-ROADMAP.md)

This roadmap is the shared target architecture for the YasinPress news-ingestion, article-intelligence, AI, queue, publishing, monitoring, PWA, scheduler and recovery pipeline. It explicitly distinguishes repository-verified implementation from planned production behavior.

### Slack Integration

- [Yasin ↔ Slack Integration Architecture](docs/architecture/YASIN_SLACK_INTEGRATION.md)

Slack is defined as a Human ↔ Yasin operational interface for communication, notifications, alerts, controlled commands, and agent interaction. YasinHub remains the Control Plane and source of truth; Slack must not bypass YasinHub to directly control the Agent Runtime.

## Ecosystem Startup Contract

All Yasin services that expose local listening ports should converge on a single canonical startup entrypoint. The startup command must be safe to repeat and must own its preflight/recovery behavior.

The contract is:

- Check the configured/default service port before starting.
- If the port is free, start normally.
- If the port is occupied, identify the current process before mutating anything.
- Terminate and replace a process only when it is positively identified as the same managed Yasin service instance.
- After termination, verify that the old process has exited and the port has actually been released before starting the replacement.
- If the port belongs to another or unrecognized program, fail closed, report the conflict, and never kill or modify that process.
- A successful termination request by itself is not sufficient evidence of recovery.

This is a cross-ecosystem operational contract, not permission for one service to manage unrelated services. Implementation details remain owned by each service repository, while Yasin-Operations defines the operational expectations and YASIN-DOCS defines the ecosystem-level contract.

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
