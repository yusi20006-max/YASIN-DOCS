# Yasin Ecosystem — Deployment Evidence Audit

**Phase:** 6 — System Graphs  
**Status:** Consolidated evidence pass

## Objective

Separate verified runtime/deployment evidence from architecture assumptions. Absence of a search result is not proof of absence.

## Current Evidence

The current repository audit does **not** establish a common Docker, Kubernetes, systemd, or reverse-proxy deployment layer across the Yasin ecosystem. Therefore the ecosystem architecture remains deployment-agnostic until source evidence establishes a canonical production topology.

## Logical Deployment Classes

| Component | Logical class | Certainty |
|---|---|---|
| Yasin-Core | Python library/runtime foundation | High |
| Yasin-Agent | Agent application/runtime | High |
| Yasin-AI | AI capability/application platform | High |
| YasinHub | Management/application runtime | High |
| YasinRelay | Long-running processing service | High |
| YasinFeed | Content processing/publishing application | Medium |
| YasinPress | News/content processing application | Medium |
| YasinCLI | Operator CLI | High |
| TJC | Developer automation CLI | High |
| YASIN-DOCS | Documentation system | High |

## Deployment Patterns

These are architecture patterns only, not claims about current production:

```text
Local
  Developer / Termux / workstation

Service host
  Long-running Yasin services

Hybrid
  Local control plane + remote runtimes
```

## Not Established

No repository-wide evidence currently establishes:

- Docker Compose as canonical deployment;
- Kubernetes as canonical deployment;
- systemd as canonical supervisor;
- a specific cloud provider;
- reverse proxy/API gateway;
- service mesh;
- shared message broker;
- shared container registry;
- common production host;
- common port allocation;
- automatic zero-downtime deployment.

## Deployment Contract

For every independently deployable component, the final audit should record:

```text
Build → Artifact → Start command → Environment → Secrets
→ Network → Storage → Health checks → Logs/metrics
→ Restart policy → Upgrade/rollback
```

## CLI vs Supervisor

A CLI command such as `start`, `stop`, `restart`, or `status` is a control-plane interface. It does not prove that the CLI owns the underlying process. The implementation must be source-verified for each command.

## AI Maintainer Rule

Before changing deployment behavior, inspect entrypoints, lifecycle code, config loaders, CI/CD workflows, service definitions, container definitions, deployment scripts, health checks, and rollback procedures. If evidence is missing, document the gap rather than inventing infrastructure.

## Phase 6 Result

The ecosystem now has an explicit **deployment evidence boundary**: documented runtime roles are separated from unverified production infrastructure.
