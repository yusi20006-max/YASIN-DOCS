# Yasin Ecosystem — Runtime & Deployment Topology

**Phase:** 6 — System Graphs  
**Status:** Refinement pass 4

## 1. Purpose

This document distinguishes what each Yasin component is at runtime from how it may be deployed. Runtime class is evidence-based where repository documentation supports it; host, container, port, supervisor, and network topology are not invented.

## 2. Runtime Classes

```text
Yasin-Core
  → library / runtime foundation

Yasin-Agent
  → agent application / task runtime

Yasin-AI
  → platform / service-capability runtime

YasinHub
  → management / registry application

YasinRelay
  → long-running service / daemon

YasinFeed
  → content ingestion/generation/publishing application

YasinPress
  → news/content processing application

YasinCLI
  → operator/developer CLI

TJC
  → developer automation CLI/tooling

Termux Backup Manager
  → operational backup utility

YASIN-DOCS
  → documentation/knowledge system
```

## 3. Logical Process Topology

```text
                    Operator / Developer
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
             YasinCLI               TJC
                 │
        ┌────────┼────────┬─────────┐
        ▼        ▼        ▼         ▼
      Core     Agent     Hub       Relay
        │        │        │         │
        └────────┴────────┴─────────┘
                         │
                         ▼
                Ecosystem capabilities

Content path:

External Sources
      │
      ▼
Feed / Relay / Press processing
      │
      ▼
AI / normalization / validation
      │
      ▼
Publishing / external destinations
```

This is a logical topology, not a claim that all components run on one machine.

## 4. Process Boundaries

### Yasin-Core

Core should be treated as an embeddable/runtime library boundary unless a deployment-specific executable is directly evidenced.

### Yasin-Agent

Agent is an executable application layer that can consume Core capabilities. It may be started by a CLI or another orchestrator, but the exact supervisor is deployment-specific.

### YasinHub

Hub is a management/application boundary. Its registry, health, events, logs, and dashboard capabilities should be treated as one logical management domain unless source proves further process separation.

### YasinRelay

Relay is a service/daemon boundary. It should be treated as independently lifecycle-managed from Core even where Core contains integration/embedded surfaces.

### YasinCLI

CLI is an operator control boundary. It should not be treated as a runtime dependency of every application merely because it can manage them.

## 5. Deployment Abstraction

The ecosystem can be deployed using multiple strategies without changing the logical architecture:

```text
Strategy A — Local development
Developer machine / Termux
    ├── CLI
    ├── Core
    ├── Agent
    ├── Hub
    └── Relay

Strategy B — Service-oriented deployment
Host / VM / container environment
    ├── Hub service
    ├── Relay service
    ├── Agent workers
    └── supporting services

Strategy C — Hybrid
Local CLI + remote services
    ├── YasinCLI / TJC locally
    └── Hub / Relay / AI remotely
```

These are supported deployment patterns, not claims about the currently deployed production topology.

## 6. Lifecycle Ownership

```text
YasinCLI
   │
   ├── discover
   ├── start
   ├── stop
   ├── restart
   ├── status
   ├── health
   └── logs
```

Lifecycle commands are control-plane capabilities. Actual process supervision may be delegated to the host/service manager.

## 7. Network Boundary Model

No fixed port map is asserted here without source evidence.

The expected boundary model is:

```text
Internet / External APIs
          │
      Network Boundary
          │
   ┌──────┴────────┐
   │ Yasin Services │
   └──────┬────────┘
          │
    Internal APIs
          │
   Runtime components
```

The next audit should enumerate actual HTTP, WebSocket, IPC, subprocess, queue, and file-based transport mechanisms.

## 8. Deployment Configuration Questions

For each service, the final topology must eventually answer:

- entry command;
- working directory;
- process owner;
- environment variables;
- secret sources;
- ports/listeners;
- outbound network dependencies;
- persistent volumes;
- health checks;
- restart policy;
- logs;
- metrics;
- backups;
- upgrade/rollback procedure.

## 9. AI-Agent Maintenance Rules

An AI coding agent must not assume:

- Docker is the deployment mechanism;
- systemd is the process supervisor;
- all services share one host;
- localhost implies production topology;
- CLI lifecycle commands imply direct process ownership;
- a library is a daemon;
- a daemon must expose HTTP;
- repositories are independently deployable just because they are separate Git repositories.

Each claim must be supported by repository evidence or explicitly labeled as deployment design.

## 10. Current Open Evidence Gaps

- exact production hosts;
- containerization;
- systemd/supervisor configuration;
- port map;
- service discovery;
- reverse proxy/API gateway;
- queues and brokers;
- WebSocket/IPC topology;
- persistent volume topology;
- production health/readiness probes;
- release/deployment automation.
