# Yasin Architecture Decision Records

Architecture Decision Records (ADRs) preserve the important architectural decisions that shape the Yasin ecosystem.

## How to use this directory

- Read `ADR_STANDARD.md` before creating or changing an ADR.
- Treat `Accepted` ADRs as the current documented architectural intent unless a newer ADR supersedes them.
- Never delete historical decisions merely because they are no longer current.
- When implementation and an ADR disagree, verify the source and document the discrepancy.

## ADR Lifecycle

```text
Proposed → Under Review → Accepted
                         ↘ Deprecated
                         ↘ Superseded → Historical
```

## Index

| ADR | Area | Status | Decision |
|---|---|---|---|
| ADR-0001 | Ecosystem structure | Proposed | Yasin is maintained as a coordinated multi-repository ecosystem with explicit ownership boundaries. |
| ADR-0002 | Core/runtime | Proposed | Yasin-Core is the foundation boundary for reusable runtime abstractions. |
| ADR-0003 | Agent architecture | Proposed | Agent orchestration is separated from the foundational runtime. |
| ADR-0004 | Management/control | Proposed | YasinHub provides the ecosystem management/status boundary. |
| ADR-0005 | Relay/pipeline | Proposed | YasinRelay owns relay and pipeline responsibilities rather than becoming a universal application layer. |
| ADR-0006 | Unified CLI | Proposed | YasinCLI is a control surface over ecosystem components, not the owner of their underlying runtime logic. |
| ADR-0007 | AI/provider boundary | Proposed | AI/provider capabilities are kept behind explicit Yasin-AI boundaries rather than duplicated across consumers. |
| ADR-0008 | Storage ownership | Proposed | Storage ownership remains component-scoped unless a shared store is explicitly designed and verified. |
| ADR-0009 | Security/trust | Proposed | Plugin/tool execution must have an explicit trust boundary; in-process execution is not automatically a sandbox. |
| ADR-0010 | Documentation | Proposed | YASIN-DOCS is the centralized architecture, decision, evidence, and AI-handoff knowledge layer. |

## Status Note

The initial ADR set above captures **candidate architectural decisions** derived from the current YASIN-DOCS baseline. They are intentionally `Proposed` until the decision is reviewed against the relevant source repositories and accepted.

## Reading Order

For a new AI agent:

1. `ADR_STANDARD.md`
2. Relevant accepted ADRs
3. Relevant proposed ADRs when investigating architectural intent
4. The affected project's architecture document
5. The actual repository source/config/tests

## Relationship to Architecture Documentation

ADRs answer **why** a significant architectural decision exists.

Architecture documents explain **what** the system currently looks like.

Source code/configuration/tests provide evidence of **what is actually implemented**.

These layers must not be conflated.
