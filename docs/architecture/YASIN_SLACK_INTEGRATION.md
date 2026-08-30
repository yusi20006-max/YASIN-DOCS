# Yasin ↔ Slack Integration Architecture

**Status:** Proposed architecture
**Scope:** Yasin ecosystem, with YasinHub as the integration/control boundary
**Primary role of Slack:** Human communication, notifications, operational commands, and agent interaction
**Source of truth:** YasinHub and the underlying Yasin services; Slack is not a system-of-record

## 1. Purpose

This document defines the target architecture for integrating the Yasin ecosystem with Slack.

The integration is designed to make Slack an operational interface for Yasin without turning Slack into the backend, execution engine, or source of truth.

The same boundary model should remain compatible with other interfaces such as Telegram, PWA/mobile control surfaces, and future integrations.

## 2. Architectural Principle

> **Slack is a Human ↔ Yasin Operational Interface, not the Yasin backend.**

YasinHub remains the Control Plane and authoritative source for execution state, events, orchestration, and cross-project integration.

Slack must communicate with Yasin through a controlled adapter boundary rather than directly invoking the Agent Runtime.

## 3. Target Architecture

```text
                         HUMAN
                           |
            +--------------+--------------+
            |                             |
          Slack                        Telegram
            |                             |
            +--------------+--------------+
                           |
                       YASINHUB
                    Control Plane
                           |
                 +---------+---------+
                 |                   |
            Yasin-Agent          Event Bus
                 |                   |
       +---------+---------+         |
       |         |         |         |
    GitHub    Yasin-AI  Yasin-Core   |
       |         |         |         |
       +---------+---------+---------+
                           |
                      Notifications
                           |
                           v
                         Slack
```

## 4. Responsibilities

### Slack

Slack provides:

- human-to-Yasin interaction;
- operational notifications;
- execution progress summaries;
- alerts;
- lightweight operational commands;
- threaded execution timelines;
- interactive controls where appropriate.

Slack does **not** own:

- canonical execution state;
- agent memory;
- repository state;
- workflow orchestration;
- authorization policy as the sole authority;
- long-term audit history.

### YasinHub

YasinHub is the integration and control boundary for Slack. It owns or coordinates:

- command routing;
- execution creation and state;
- event normalization;
- integration authorization;
- correlation between Slack conversations and Yasin executions;
- delivery/retry handling for outbound notifications;
- links to GitHub, Yasin-Agent, Yasin-Core, and Yasin-AI.

### Yasin-Agent

Yasin-Agent remains the execution layer. Slack must not bypass YasinHub to directly control the Agent Runtime.

### GitHub / Yasin-Core / Yasin-AI

These components retain their existing responsibilities. Slack only exposes selected operational information through YasinHub.

## 5. Slack App

Yasin should use a dedicated Slack App with a Bot User, conceptually represented as:

```text
@Yasin
```

Initial channels:

```text
#yasin
#yasin-alerts
#yasin-agent
```

Additional channels such as `#yasin-ci` or `#yasin-deployments` should only be introduced when message volume or operational separation justifies them.

## 6. Integration Boundary

The recommended flow is:

```text
Slack Event
    |
    v
Slack Adapter
    |
    +-- verify request/signature
    +-- authenticate actor
    +-- authorize action
    +-- normalize event
    |
    v
YasinHub
    |
    v
ExecutionRuntime / Event System
    |
    v
Yasin-Agent
```

The inverse notification flow is:

```text
Yasin Event
    |
    v
YasinHub
    |
    v
Slack Adapter
    |
    v
Slack API
```

## 7. Adapter Design

The implementation should provide a dedicated Slack integration boundary, conceptually structured as:

```text
integrations/slack/
├── client.py
├── events.py
├── commands.py
├── formatter.py
├── permissions.py
└── router.py
```

The exact package location must be reconciled with the repository's verified structure before implementation.

Responsibilities:

- `client`: Slack API transport;
- `events`: inbound Slack event parsing and validation;
- `commands`: command registration and dispatch;
- `formatter`: human-readable Slack messages and blocks;
- `permissions`: actor/role/action authorization checks;
- `router`: mapping normalized Slack events into YasinHub operations.

## 8. Internal Event Model

Slack-specific payloads should be normalized before entering the Yasin domain.

Conceptually:

```text
Slack message
    |
    v
YasinEvent

source: slack
type: USER_COMMAND | USER_MESSAGE | INTERACTION
actor: <mapped Yasin identity>
channel: <Slack channel>
correlation_id: <request/execution correlation>
payload: <normalized command or message>
```

This prevents Slack-specific details from leaking throughout the core runtime.

## 9. Command Interface

### Phase 1 — Read-only

```text
/status
/health
/executions
/execution <id>
/help
```

Examples:

```text
@Yasin /status
@Yasin /health
@Yasin /execution exec_1842
```

### Phase 2 — Controlled operations

```text
/run <task>
/cancel <id>
/retry <id>
```

These commands require explicit authorization.

### Phase 3 — Interactive operations

Use Slack buttons/actions for selected operations such as:

```text
[View]
[Retry]
[Cancel]
[View PR]
```

### Phase 4 — Natural-language agent interaction

```text
@Yasin
Why did execution exec_1842 fail?
```

YasinHub should gather the relevant execution, GitHub, CI, and runtime information before producing the response.

## 10. Notification Model

Notifications should be event-driven and selective.

Important events include:

- execution started;
- execution completed;
- execution failed;
- execution cancelled;
- CI failed;
- deployment failed;
- deployment succeeded;
- agent unavailable;
- external dependency blocked an execution;
- other high-priority operational alerts.

Do not send every low-level runtime log to Slack. Events should be aggregated into meaningful progress updates.

## 11. Threaded Execution Timeline

Each significant execution should preferably have one root Slack message with progress in a thread.

Example:

```text
#yasin-agent

🚀 Execution #1842 started

    ├── 🔎 Repository analyzed
    ├── 🛠️ Implementation completed
    ├── 🧪 Tests passed
    ├── 🔀 PR #71 created
    └── ✅ PR #71 merged
```

This keeps operational channels readable while preserving execution context.

## 12. Alerts

`#yasin-alerts` is reserved for important operational conditions.

Severity examples:

```text
🔴 CRITICAL — service unavailable
🟡 WARNING  — execution blocked/waiting
🟢 SUCCESS  — deployment or major operation completed
```

Alerts should include a correlation/execution identifier and a link or reference to the authoritative YasinHub/GitHub record when available.

## 13. Identity and Authorization

Slack identity must be mapped to a Yasin identity before privileged actions are accepted.

Conceptually:

```text
Slack User ID
      |
      v
Identity Mapping
      |
      v
Yasin User / Role
      |
      v
Authorization Policy
      |
      v
YasinHub Operation
```

Suggested roles:

```text
VIEWER
OPERATOR
DEVELOPER
ADMIN
```

Example permission model:

| Operation | Viewer | Operator | Developer | Admin |
|---|---:|---:|---:|---:|
| `/status` | Yes | Yes | Yes | Yes |
| `/health` | Yes | Yes | Yes | Yes |
| `/executions` | Yes | Yes | Yes | Yes |
| `/execution` | Yes | Yes | Yes | Yes |
| `/run` | No | Yes | Yes | Yes |
| `/cancel` | No | Yes | Yes | Yes |
| `/retry` | No | Yes | Yes | Yes |
| deployment actions | No | No | Policy-based | Yes |

The final permission matrix must follow the canonical Yasin authorization model once one is established.

## 14. Security Requirements

The integration must include, at minimum:

- Slack request/signature verification;
- secure bot credentials and secret storage;
- actor authentication and identity mapping;
- explicit authorization checks for commands;
- channel allowlisting where appropriate;
- replay/request protection where applicable;
- correlation IDs for auditability;
- no secrets in Slack messages;
- no direct unrestricted access from Slack to the Agent Runtime;
- rate limiting and abuse protection for inbound commands;
- safe handling of interactive actions.

Slack credentials must be configuration/secret material owned by the integration deployment boundary and must never be committed to YASIN-DOCS.

## 15. Execution Lifecycle Example

A complete workflow can look like this:

```text
monday / GitHub / user request
            |
            v
         YasinHub
            |
            v
    Create Execution #1842
            |
            v
       Yasin-Agent
            |
            +--> Repository analysis
            +--> Implementation
            +--> Tests
            +--> PR creation
            +--> CI
            +--> Merge
            |
            v
         YasinHub
            |
            v
          Slack
```

Slack timeline:

```text
🚀 Execution #1842 started
🔎 Analysis completed
🛠️ Implementation completed
🧪 CI passed
🔀 PR #71 created
🎉 PR #71 merged
```

## 16. monday.com Relationship

If monday.com is used as the project/task management interface, it should remain complementary to Slack:

```text
                  YasinHub
                 /        \
                /          \
             Slack        monday.com
               |              |
       Communication     Task/Project Management
               \              /
                \            /
                 Yasin-Agent
```

Recommended separation:

- **Slack:** chat, alerts, notifications, operational interaction;
- **monday.com:** tasks, projects, assignments, status, planning;
- **YasinHub:** execution, state, events, control;
- **Yasin-Agent:** execution;
- **GitHub:** source code, issues, PRs, CI.

Neither Slack nor monday.com should replace YasinHub as the canonical execution/control layer.

## 17. Implementation Phases

### Phase 1 — Read-only integration

- Slack App and Bot User;
- request verification;
- `status`, `health`, `executions`, `execution`, `help`;
- execution start/completion/failure notifications;
- basic `#yasin`, `#yasin-alerts`, `#yasin-agent` channels.

### Phase 2 — Controlled operations

- `/run`;
- `/cancel`;
- `/retry`;
- identity mapping;
- role-based authorization;
- command audit trail.

### Phase 3 — Rich interaction

- Slack threads;
- Block Kit-style structured messages;
- interactive buttons;
- PR/CI action links;
- summarized execution progress.

### Phase 4 — Agent conversation

- natural-language interaction with `@Yasin`;
- context retrieval through YasinHub;
- execution/GitHub/CI-aware answers;
- safe tool/action selection through the existing Yasin control boundary.

## 18. Free Slack Plan

The Slack Free plan is sufficient for the initial Yasin integration when Slack is used as a communication and operational interface rather than as the data store.

The design must not depend on Slack retaining historical data indefinitely. Canonical execution and audit information must remain in Yasin-owned systems.

The initial integration should therefore minimize dependency on Slack history and keep durable state in YasinHub and the relevant source systems.

## 19. Non-Goals

This integration does not aim to:

- move Yasin's execution state into Slack;
- make Slack a database;
- make Slack the primary agent runtime;
- bypass YasinHub;
- duplicate Yasin-Core memory into Slack;
- expose unrestricted infrastructure commands to Slack users;
- make Yasin dependent on a paid Slack tier for core functionality.

## 20. Architecture Decision Summary

1. **YasinHub remains the Control Plane and source of truth.**
2. **Slack is an operational interface.**
3. **Slack commands enter Yasin through a dedicated adapter.**
4. **Slack must not directly bypass YasinHub to control Yasin-Agent.**
5. **Inbound Slack events are normalized into Yasin-domain events.**
6. **Outbound notifications are event-driven, aggregated, and correlated with executions.**
7. **Privileged operations require identity mapping and authorization.**
8. **Slack Free is acceptable for the initial implementation.**
9. **The architecture remains compatible with Telegram, monday.com, GitHub, and future interfaces.**
10. **Implementation details must be verified against the target repository before coding.**

## 21. Verification Rule

This document describes the target/proposed architecture. It does not claim that the Slack integration is already implemented.

Before implementation, the target repositories must be audited for their current APIs, event models, authentication boundaries, execution lifecycle, and integration conventions. Any mismatch between this design and the verified implementation must be documented and resolved explicitly.
