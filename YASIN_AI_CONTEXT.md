# Yasin Ecosystem — AI Context

> Primary orientation file for a new AI agent. Read this first, then follow `docs/ai/AI_INDEX.md`.

## Identity

Yasin is a multi-repository software ecosystem. YASIN-DOCS is its centralized architecture and knowledge repository.

## Core Components

| Component | Primary responsibility |
|---|---|
| Yasin-Core | Runtime/foundation abstractions |
| Yasin-Agent | Agent/task orchestration and execution |
| Yasin-AI | AI, knowledge, retrieval and provider capabilities |
| YasinHub | Ecosystem management/status |
| YasinRelay | Feed/relay ingestion and processing |
| YasinFeed | Content generation/publishing |
| YasinPress | News/content processing |
| YasinCLI | Unified operator/developer CLI |
| TJC | Developer/Jules automation |
| YASIN-DOCS | Architecture, contracts, evidence and AI handoff |

## Critical Boundaries

- Yasin-Core is the foundation; do not duplicate its runtime abstractions in consumers.
- Yasin-Agent is an agent layer; distinguish agent behavior from core runtime behavior.
- Yasin-AI owns AI/knowledge capability boundaries; do not assume every provider is globally shared.
- YasinHub is a management boundary; status data is not automatically a universal event bus.
- YasinRelay owns relay/pipeline behavior; its local APIs are not automatically ecosystem APIs.
- YasinCLI is a control surface; a CLI command does not prove ownership of the underlying process.
- Storage is component-owned unless a shared store is explicitly verified.

## Known Concrete Integration Signals

Yasin-Agent documents integration with `yasin_core.sdk` and `YasinCoreClient`.

YasinHub documents status storage through its status-store layer.

YasinRelay documents SQLite persistence and CLI/runtime pipeline boundaries.

Yasin-AI documents local SQLite-backed persistence and trusted in-process plugin execution.

These are evidence-backed starting points; inspect current source before making changes.

## Architecture Truth Model

```text
Verified → Documented → Inferred → Candidate → Unknown
```

Never move information upward in this chain without evidence.

## Work Protocol

```text
1. Identify request.
2. Select owning repository.
3. Read project architecture.
4. Inspect source/config/tests.
5. Find consumers and dependencies.
6. Classify the change.
7. Implement minimally.
8. Test.
9. Audit cross-project impact.
10. Update docs when architecture/contracts change.
11. Report evidence and limitations.
```

## AI Documentation Map

- `docs/ai/AI_INDEX.md` — complete AI documentation navigation.
- `docs/ai/AI_ONBOARDING.md` — onboarding and ecosystem orientation.
- `docs/ai/AI_OPERATING_RULES.md` — operating rules.
- `docs/ai/AI_EVIDENCE_POLICY.md` — evidence discipline.
- `docs/ai/AI_PROJECT_SELECTION_MATRIX.md` — repository ownership selection.
- `docs/ai/AI_CHANGE_IMPACT_PROTOCOL.md` — impact classification.
- `docs/ai/AI_TESTING_VALIDATION_PROTOCOL.md` — validation ladder.
- `docs/ai/AI_SECURITY_PROTOCOL.md` — security rules.
- `docs/ai/AI_GIT_WORKFLOW.md` — Git workflow.
- `docs/ai/AI_HANDOFF_PROTOCOL.md` — continuation/handoff contract.

## Architecture Map

- `docs/architecture/` — system architecture, project records, graphs and audits.
- `ROADMAP.md` — documentation phase status.

## Phase State

Phase 1–5: complete.  
Phase 6: baseline architecture graphs complete; deeper source-verification items remain explicit backlog.  
Phase 7: AI Handoff System in progress.

## Non-Negotiable Rules

- Do not invent APIs, events, endpoints, schemas, deployment infrastructure, or dependencies.
- Do not commit credentials or sensitive values.
- Do not change a cross-project contract without checking consumers.
- Do not claim tests were run when they were not.
- Do not hide uncertainty.
- Do not discard unrelated user work.

## Goal

A new AI agent should be able to use this repository to understand Yasin, select the correct project, make bounded changes, validate them, and hand work to another agent without losing architectural context.
