# ADR-0003: Separate Agent Orchestration from the Core Runtime

- Status: Proposed
- Date: 2026-08-09
- Decision owners: Yasin ecosystem maintainers
- Scope: Yasin-Agent and Yasin-Core
- Supersedes: None
- Superseded by: None

## Context

An agent system needs task orchestration, agent-specific behavior, tool coordination, and execution policy. These concerns are different from the reusable runtime abstractions provided by the foundation layer.

## Decision

Agent orchestration and agent-specific behavior belong to Yasin-Agent, while reusable foundational runtime abstractions belong to Yasin-Core.

Yasin-Agent may consume Core APIs but should not silently redefine Core responsibilities inside the agent layer.

## Rationale

Separating orchestration from foundation allows the runtime to remain reusable while agents can evolve task-oriented behavior independently.

## Alternatives Considered

### Put agent orchestration into Core
Rejected because it would couple the foundation to a particular agent model.

### Keep agents completely independent of Core
Rejected because it would duplicate reusable runtime behavior and weaken common contracts.

## Consequences

### Positive

- Clear agent ownership.
- Reusable Core runtime.
- More focused testing.
- Easier evolution of agent strategies.

### Negative / Trade-offs

- Integration contracts must remain compatible.
- Some features may require coordinated Core and Agent changes.

### Operational

Agent lifecycle and task behavior should be tested at the Agent layer, while foundational runtime behavior should be tested at Core.

## Architecture Impact

Creates a primary architectural boundary between runtime foundation and agent orchestration.

## Evidence

- `YASIN_AI_CONTEXT.md`
- `docs/ai/AI_PROJECT_SELECTION_MATRIX.md`
- Yasin-Agent architecture/integration documentation
- Existing references to Yasin-Agent consuming `yasin_core.sdk` / `YasinCoreClient`

Exact source-level contracts remain subject to verification.

## Related Documents

- ADR-0001
- ADR-0002
- `docs/ai/AI_CHANGE_IMPACT_PROTOCOL.md`

## Open Questions

- Which Agent APIs should be considered ecosystem-wide contracts?
- Where should agent lifecycle state be owned and persisted?
