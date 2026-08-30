# ADR — External Control Plane: monday.com → YasinHub → Yasin-Agent → GitHub

- Date: 2026-08-30
- Status: **Accepted / Implemented**
- Scope: YasinHub, Yasin-Agent, monday.com, GitHub
- Implementation tracking: `yusi20006-max/YasinHub` Issues #64–#68

## Context

YasinHub is the ecosystem Control Plane and Observability Plane. Yasin-Agent is the execution boundary for agent/workflow work, while GitHub remains authoritative for source code, branches, pull requests, reviews, and CI state.

monday.com provides the external planning, task-management, visibility, and human-control surface. It must not become an execution runtime or couple directly to Yasin-Agent.

## Decision

Adopt and implement the following architecture:

```text
monday.com
    │ Webhook / GraphQL
    ▼
YasinHub Control Plane
    │
    ├─ Event normalization
    ├─ Authentication / authorization
    ├─ Idempotency / correlation
    ├─ Policy / approvals
    ├─ Execution lifecycle
    └─ Audit
    │
    ▼
Execution Runtime → Yasin-Agent
    │
    ▼
GitHub: Issue → Branch → PR → CI
    │ Webhooks
    ▼
YasinHub → monday synchronization
```

### Responsibility boundaries

| Component | Responsibility |
|---|---|
| monday.com | Planning, task visibility, operator interaction, human-control surface |
| YasinHub | Orchestration, auth, policy, execution lifecycle, normalization, correlation, idempotency, audit, synchronization |
| Yasin-Agent | Executes authorized work; remains monday-agnostic |
| GitHub | Authoritative repository, branch, Issue, PR, review, and CI facts |

## Implemented Integration

The architecture has been implemented in YasinHub through five sequential Issues and merged PRs:

| Issue | Implementation | PR | Status |
|---|---|---|---|
| #64 | monday foundation, webhook ingress, challenge/signature verification, normalization, health/sync | #69 | **Merged** |
| #65 | `task.ready` → validation → Execution Runtime → Agent boundary; idempotent start/cancel/retry | #74 | **Merged** |
| #66 | GitHub PR/review/check Webhook bridge, verification, correlation, state updates | #75 | **Merged** |
| #67 | Bidirectional monday ↔ YasinHub synchronization, configurable columns, reconciliation, loop prevention | #76 | **Merged** |
| #68 | Control Plane policy, default-deny privileged operations, approval, idempotent controls, audit | #77 | **Merged** |

All five PRs were squash-merged and CI was green before merge. Existing test coverage remained green; dedicated integration tests were added for the five implementation areas.

## Internal Event Boundary

Raw monday/GitHub payloads are not part of the core runtime contract.

```text
monday payload → Monday Adapter → normalized Yasin Event
GitHub payload → GitHub Adapter → normalized Yasin Event
```

Normalized events preserve external identifiers and, where applicable, `execution_id`, `correlation_id`, actor, source, timestamp, and state/action data.

## Execution Flow

```text
monday Status = Ready
        ↓
Webhook ingress
        ↓
Verification / validation
        ↓
Event normalization + idempotency
        ↓
Authorization / policy
        ↓
Execution creation or recovery
        ↓
Execution Runtime / AgentRuntimeAdapter
        ↓
Yasin-Agent
        ↓
GitHub Issue / Branch / PR / CI
        ↓
GitHub Webhook
        ↓
YasinHub correlation + state update
        ↓
Policy / approval when required
        ↓
monday synchronization
```

Yasin-Agent contains no monday-specific logic.

## State Model

The implementation intentionally reuses the existing YasinHub core execution states rather than breaking Agent contracts by expanding the core transition table. Higher-level lifecycle concepts such as `PR_OPEN`, `CI_RUNNING`, and `MERGED` are represented through metadata/status transitions mapped to monday.

Core states include:

```text
queued → running → paused → succeeded
                   ├→ failed
                   └→ cancelled
```

The external lifecycle is therefore a projection over the existing execution model, not a second state machine.

## Idempotency and Correlation

External Webhooks are treated as at-least-once delivery and may be duplicated or arrive out of order.

Idempotency is implemented for external events and control operations, including start, cancel, retry, re-run, and approvals. Control events use a stable `control_event_id` and approvals are bound to `execution_id:action`.

The lifecycle is traceable as:

```text
monday item
  ↓
execution_id / correlation_id
  ↓
Yasin-Agent run
  ↓
GitHub Issue / PR
  ↓
CI / Checks
```

## Bidirectional Synchronization

```text
monday ↔ YasinHub ↔ GitHub
```

YasinHub is authoritative for orchestration/execution state; GitHub is authoritative for repository/PR/CI facts; monday is the operator-facing planning/visibility surface.

Implemented capabilities include configurable monday column mapping, event-driven updates, reconciliation, retries, missing-resource handling, idempotency, and loop prevention.

## Security and Governance

Implemented controls include:

- monday challenge handling and optional HMAC verification
- GitHub `X-Hub-Signature-256` verification when configured
- credentials from environment/configuration rather than board items
- secret redaction in audit/execution metadata
- default-deny privileged operations
- approval binding to `execution_id:action`
- idempotent control events
- rejection of unverified Webhooks before state mutation

Live monday GraphQL writes safely operate in dry-run mode when `YASINHUB_MONDAY_API_TOKEN` is absent. Live writes require the real API token and configured column IDs.

## Control Surfaces

monday is the first implemented external control surface. The same YasinHub control boundary is intentionally reusable by:

```text
monday ─┐
PWA ────┤
CLI ────┤ → YasinHub Control API → Execution Runtime → Yasin-Agent
Telegram┤
Slack ──┘
```

A new surface must not require monday-specific or channel-specific logic inside Yasin-Agent.

## Verification

Implementation evidence:

- YasinHub #64 / PR #69
- YasinHub #65 / PR #74
- YasinHub #66 / PR #75
- YasinHub #67 / PR #76
- YasinHub #68 / PR #77

Reported verification: all five PRs CI-green; existing suite remained green; integration tests cover happy paths, invalid payloads, verification failures, duplicates, correlation, cancellation, policy deny/approve, and audit behavior.

## Remaining Technical Debt

The defined #64–#68 scope is complete with no blockers. Follow-up work may include:

1. Configure production monday API credentials and real board column IDs.
2. Tighten PR/CI-to-execution matching with dedicated GitHub correlation metadata where useful.
3. Expand the core lifecycle only if future Agent contracts explicitly require it.
4. Add a richer PWA approval UI for privileged operations.
5. Add additional external control surfaces using the same Control API.

## Consequences

### Positive

- monday can safely initiate and observe Yasin work without coupling to the Agent.
- YasinHub centralizes policy, execution, correlation, idempotency, and audit.
- GitHub remains authoritative for code and CI facts.
- New control surfaces can be added without changing Agent domain logic.

### Trade-offs

- YasinHub must maintain external adapters and reconciliation logic.
- Webhook retries and external API evolution add operational complexity.
- Production monday writes require external credentials and board configuration.

## Status

**Accepted / Implemented.** The architecture is implemented through YasinHub Issues #64–#68 and PRs #69, #74, #75, #76, and #77.