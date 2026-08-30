# ADR — Yasin Control Plane Productionization

- Date: 2026-08-30
- Status: **Proposed / Next Phase**
- Scope: YasinHub Control Plane, monday integration, PWA, GitHub correlation, external control surfaces
- Depends on: `ADR-00X-EXTERNAL-CONTROL-PLANE-MONDAY-YASINHUB-GITHUB.md`

## Context

The monday → YasinHub → Yasin-Agent → GitHub Control Plane is implemented through YasinHub Issues #64–#68 and PRs #69, #74, #75, #76, and #77.

The next objective is not to add another execution path. It is to productionize the existing Control Plane so that external control surfaces can safely operate the same execution lifecycle.

The immediate priority is to move from integration-complete to operationally complete:

```text
implemented adapters
        ↓
real external configuration
        ↓
strong correlation
        ↓
operator control UI
        ↓
production observability
        ↓
additional control surfaces
```

## Decision

The next development phase is **Yasin Control Plane Productionization**.

YasinHub remains the single orchestration and policy boundary. No new control surface may directly invoke Yasin-Agent or GitHub privileged operations.

## Phase Objectives

### 1. Live monday Integration

Move the implemented monday integration from safe dry-run capability to verified live operation.

Requirements:

- production API credential configuration
- board ID configuration
- column mapping configuration
- webhook registration and verification
- live read/write validation
- retry and rate-limit handling
- reconciliation after missed events
- secret-safe diagnostics

Dry-run remains the safe default when production credentials are absent.

### 2. Strong Execution Correlation

Strengthen the relationship between:

```text
monday item
    ↕
execution_id
    ↕
agent run
    ↕
GitHub Issue
    ↕
branch
    ↕
PR
    ↕
CI/checks
```

Correlation metadata should be stable, queryable, and recoverable after restarts.

Where practical, GitHub PR/Issue metadata should contain a non-secret Yasin execution/correlation reference so webhook events can be matched deterministically.

### 3. YasinHub PWA Control Surface

Extend the existing YasinHub PWA into an operator control surface.

Minimum capabilities:

- execution list/detail
- execution timeline
- agent status
- GitHub Issue/PR/CI links
- monday item reference
- approve
- reject
- cancel
- retry
- re-run
- policy decision visibility
- audit history

The PWA must call YasinHub Control APIs rather than implementing policy itself.

### 4. Unified Control API

Define one stable internal/external control contract for actions such as:

```text
start
cancel
retry
re-run
approve
reject
```

All surfaces use this contract:

```text
monday ─┐
PWA ────┤
CLI ────┤
Telegram┤
Slack ──┘
    ↓
YasinHub Control API
    ↓
Policy / Authorization
    ↓
Execution Runtime
    ↓
Yasin-Agent
```

The Control API must enforce authentication, authorization, idempotency, correlation, and audit consistently.

### 5. Production Observability

Every external control action and execution transition should be observable through:

- structured events
- execution timeline
- correlation identifiers
- audit records
- health/readiness information
- failure reason and retry metadata

Avoid logging secrets or sensitive credentials.

## Proposed Implementation Sequence

```text
Phase 2.1  Live monday + configuration
     ↓
Phase 2.2  Strong GitHub/Execution correlation
     ↓
Phase 2.3  Unified Control API hardening
     ↓
Phase 2.4  PWA operator controls
     ↓
Phase 2.5  Production observability + reconciliation
     ↓
Phase 3    Slack Control Surface
```

The sequence may be adjusted if repository dependencies require a different order, but no new external surface should bypass the unified Control API.

## Acceptance Criteria

The phase is considered production-ready when an operator can:

1. Create or identify a task in monday.
2. See its YasinHub execution.
3. Identify the associated Agent run.
4. Identify the GitHub Issue/PR and CI state.
5. Approve or reject a policy-gated action.
6. Cancel/retry/re-run through YasinHub.
7. See the resulting state synchronized back to monday.
8. Reconstruct the full lifecycle through correlation and audit records.
9. Recover from duplicate/missed/out-of-order external events without duplicate privileged actions.

## Security Requirements

- default-deny for privileged operations
- verified monday/GitHub Webhooks
- environment/secret-manager based credentials
- no secrets in monday items
- no secrets in audit logs
- idempotent control actions
- approval bound to exact execution/action
- least-privilege external credentials
- policy evaluation centralized in YasinHub

## Non-Goals

This phase does not:

- create a second Agent runtime
- make Yasin-Agent aware of monday, Slack, or PWA
- make monday authoritative for execution state
- replace GitHub as the source of repository/PR/CI facts
- duplicate policy logic in clients

## Future Control Surfaces

Once the unified Control API is production-ready, Slack becomes the next recommended external surface.

Slack should provide conversational access such as:

```text
@yasin status execution exec_8127
@yasin retry exec_8127
@yasin approve exec_8127 merge
```

These are requests to YasinHub, not direct Agent commands.

The same model can later support CLI and Telegram without changing the execution core.

## Rationale

Productionizing the existing Control Plane before adding Slack reduces architectural duplication and creates one reliable contract for all future interfaces.

The intended end state is:

```text
                 ┌──────────────┐
                 │   monday     │
                 └──────┬───────┘
                        │
┌────────────┐          │          ┌────────────┐
│    PWA     ├──────────┼──────────┤   Slack    │
└────────────┘          │          └────────────┘
                        ▼
                ┌────────────────┐
                │    YasinHub    │
                │ Control Plane  │
                └───────┬────────┘
                        │
                Policy / Audit /
                Correlation /
                Idempotency
                        │
                        ▼
                Execution Runtime
                        │
                        ▼
                  Yasin-Agent
                        │
                        ▼
                     GitHub
```

## Status

**Proposed / Next Phase.** The monday/GitHub integration foundation is implemented; this ADR defines the next engineering phase before introducing Slack as an additional control surface.
