# ADR — External Control Plane: monday.com → YasinHub → Yasin-Agent → GitHub

- Date: 2026-08-30
- Status: Accepted / Implementation in progress
- Scope: YasinHub, Yasin-Agent, monday.com, GitHub
- Implementation tracking: `yusi20006-max/YasinHub` Issues #64–#68

## Context

YasinHub is the ecosystem Control Plane and Observability Plane. Yasin-Agent is the execution boundary for agent/workflow work, while GitHub remains the authoritative system for source code, branches, pull requests, reviews, and CI state.

The ecosystem needs an external human-facing control surface that can create and manage work without coupling external products directly to the Agent runtime. monday.com is selected as a planning, task-management, visibility, and human-approval surface.

The integration must preserve YasinHub as the orchestration authority and must not make Yasin-Agent aware of monday.com.

## Decision

Adopt the following control-plane architecture:

```text
                         monday.com
                    Planning / Control UI
                            │
                    Webhook / GraphQL API
                            │
                            ▼
                    ┌────────────────┐
                    │    YasinHub    │
                    │ Control Plane  │
                    └───────┬────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
       Event Normalize   Policy       Idempotency /
       + Correlation     /Auth         Correlation
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                    Execution Runtime
                            │
                            ▼
                      Yasin-Agent
                            │
                            ▼
                         GitHub
                 Issue → Branch → PR → CI
                            │
                       GitHub Webhooks
                            │
                            ▼
                        YasinHub
                            │
                            ▼
                         monday.com
```

### Responsibility boundaries

| Component | Responsibility |
|---|---|
| monday.com | Task planning, status visibility, operator interaction, human approval surface |
| YasinHub | Orchestration, authentication, authorization, execution lifecycle, event normalization, correlation, idempotency, policy, audit, synchronization |
| Yasin-Agent | Executes authorized work; remains monday-agnostic |
| GitHub | Authoritative repository, Issue, branch, PR, review, and CI state |

monday.com is not an execution runtime. It may request an action, but YasinHub validates and authorizes the action before execution.

## Internal Event Boundary

Raw external payloads must never be exposed directly to the core execution runtime.

```text
monday payload → Monday Adapter → normalized Yasin Event
GitHub payload → GitHub Adapter → normalized Yasin Event
```

The normalized event should preserve, as applicable:

- source
- event type
- external event/item identifier
- board/item/repository identifiers
- `execution_id`
- `correlation_id`
- actor information
- timestamp
- relevant state/action data

The runtime consumes the internal event contract rather than monday/GitHub-specific payload formats.

## Execution Flow

A monday item becomes executable only when its state and policy permit it.

```text
monday Status = Ready
        ↓
Webhook ingress
        ↓
Authentication / validation
        ↓
Event normalization
        ↓
Authorization / policy
        ↓
Create or recover execution
        ↓
Dispatch Yasin-Agent
        ↓
Agent works against GitHub
        ↓
Issue / Branch / PR / CI
        ↓
GitHub Webhook
        ↓
YasinHub state update
        ↓
Synchronize monday
```

The webhook handler must not directly launch an Agent without passing through the existing execution/runtime boundary.

## Idempotency

External webhook delivery is assumed to be at-least-once and may contain duplicates or out-of-order events.

The integration therefore requires idempotency for:

- monday events
- GitHub events
- execution creation
- retry
- cancellation
- re-run
- approval/rejection
- synchronization

A duplicate event must not create a second execution or repeat a privileged action.

## Correlation Model

The integration must preserve a traceable relationship:

```text
monday item
    │
    ▼
execution_id / correlation_id
    │
    ▼
Yasin-Agent run
    │
    ▼
GitHub Issue
    │
    ▼
Pull Request
    │
    ▼
CI / Checks
```

This allows the complete lifecycle of a task to be reconstructed from YasinHub.

## State Model

Reuse or extend the existing YasinHub execution state model. Do not introduce a parallel lifecycle implementation.

Target lifecycle:

```text
BACKLOG
  ↓
READY
  ↓
QUEUED
  ↓
RUNNING
  ↓
PR_OPEN
  ↓
CI_RUNNING
  ↓
REVIEW
  ↓
MERGED
  ↓
DONE
```

Failure/cancellation paths include:

```text
RUNNING → FAILED
CI_RUNNING → CI_FAILED → RUNNING
RUNNING → CANCELLED
```

monday status is a synchronized representation of the lifecycle, not a replacement for the YasinHub execution state machine.

## Bidirectional Synchronization

The desired relationship is:

```text
monday ↔ YasinHub ↔ GitHub
```

YasinHub remains authoritative for orchestration and execution state.

GitHub remains authoritative for repository/PR/CI facts.

monday remains the operator-facing planning and visibility surface.

Synchronization must support:

- configurable monday board/column mappings
- event-driven updates
- reconciliation for missed webhooks
- retry
- missing-resource handling
- loop prevention
- idempotency

## Security and Governance

Credentials and secrets must remain outside monday items and normal audit records.

Incoming Webhooks must be authenticated/verified before they can mutate state.

Privileged operations must pass YasinHub authorization and policy checks. Policy may evaluate:

- Agent
- repository
- branch
- operation
- actor
- execution

Operations such as production merge may require explicit human approval.

Approval must be bound to the exact execution/action being approved and must itself be idempotent.

Every important control operation must produce an audit record containing, where applicable:

- actor
- source
- timestamp
- `correlation_id`
- `execution_id`
- external identifiers
- policy decision
- action
- outcome

Secrets must never be written to the audit trail.

## Control Surfaces

monday is one external control surface. The architecture intentionally allows additional surfaces such as YasinCLI, PWA, Telegram, and future Slack integration to use the same YasinHub control boundary.

```text
monday ─┐
PWA ────┤
CLI ────┤ → YasinHub Control API → Execution Runtime → Yasin-Agent
Telegram┤
Slack ──┘
```

Adding a new control surface must not require changes to the Agent's domain logic.

## Implementation Plan

The implementation is tracked in YasinHub through the following ordered Issues:

1. **#64 — monday foundation**
   - integration boundary
   - configuration
   - webhook ingress
   - verification
   - normalization
   - health/sync endpoints where appropriate

2. **#65 — monday → Runtime → Agent**
   - task validation
   - authorization
   - execution creation
   - dispatch
   - start/cancel/retry
   - idempotency and correlation

3. **#66 — GitHub event bridge**
   - PR lifecycle
   - review lifecycle
   - CI/check lifecycle
   - signature verification
   - normalization and correlation

4. **#67 — bidirectional state synchronization**
   - monday ↔ YasinHub state mapping
   - configurable columns
   - reconciliation
   - retry and loop prevention

5. **#68 — Control Plane governance**
   - approval/rejection
   - policy enforcement
   - cancel/retry/re-run controls
   - audit trail

Implementation order is strictly #64 → #65 → #66 → #67 → #68.

## Non-Goals

This decision does not:

- make monday the Yasin execution runtime
- make Yasin-Agent depend on monday
- replace GitHub with monday
- introduce a second execution runtime
- require a shared application database
- make monday-specific payloads part of core runtime contracts

## Consequences

### Positive

- External task management can control Yasin safely through a stable boundary.
- Yasin-Agent remains reusable and vendor-neutral.
- GitHub remains the source of truth for code and CI facts.
- All execution paths can share YasinHub authorization, correlation, idempotency, and audit mechanisms.
- Additional control surfaces can be added without changing Agent business logic.

### Trade-offs

- YasinHub must maintain external adapters and synchronization logic.
- Webhook delivery, retries, and reconciliation add operational complexity.
- monday/GitHub API changes must be isolated behind adapters.

## Evidence / Related Work

- YasinHub is established as the ecosystem Control Plane in the Yasin ecosystem architecture baseline.
- Current YasinHub runtime boundaries include `AgentRuntimeAdapter` and existing execution observation/state infrastructure.
- Implementation tracking: YasinHub Issues #64–#68.
- monday.com provides GraphQL API and webhook capabilities for board/item integrations.
- GitHub provides Webhooks for pull requests, reviews, checks, and related repository events.

## Status

Accepted architecture. Implementation is in progress under YasinHub Issues #64–#68.
