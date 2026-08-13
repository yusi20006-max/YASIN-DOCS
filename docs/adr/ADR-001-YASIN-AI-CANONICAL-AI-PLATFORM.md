# ADR-001 — Yasin-AI as the Canonical AI Platform

- Status: Accepted
- Date: 2026-08-14
- Scope: Entire Yasin ecosystem

## Context

Yasin contains multiple projects that require AI capabilities: Yasin-Agent, YasinRelay, YasinFeed, YasinPress, and future ecosystem services. Historically, these projects have had local AI/provider abstractions. Without a central ownership decision, the ecosystem risks duplicating provider routing, model management, memory, knowledge/RAG, embeddings, observability, and AI security logic across repositories.

Yasin-Core remains the generic runtime foundation, Yasin-Agent owns agent/workflow execution, YasinHub owns ecosystem control/observability, and YasinCLI owns the unified user-facing command surface. None of these roles should absorb ownership of the ecosystem-wide AI platform.

## Decision

**Yasin-AI is the canonical AI capability platform for the Yasin ecosystem.**

Yasin-AI owns shared AI infrastructure and capabilities, including:

- model/provider abstraction and routing;
- inference-facing AI services;
- embeddings and semantic retrieval primitives;
- knowledge/RAG capabilities;
- durable AI memory;
- AI extension/plugin contracts;
- AI-specific observability and diagnostics;
- AI service/API/SDK contracts;
- centralized provider reliability/fallback policies where appropriate.

Projects retain ownership of their own domain logic:

- Core owns generic runtime/SDK foundations.
- Agent owns agent planning/execution semantics.
- Hub owns ecosystem control and lifecycle orchestration.
- CLI owns user-facing orchestration.
- Relay, Feed, and Press own content/business pipelines.

## Integration Rule

The canonical AI platform decision does **not** require projects to import Yasin-AI private implementation modules.

The intended boundary is:

```text
Project / Agent
      │
      ▼
Versioned AI Capability Contract
      │
      ▼
  Yasin-AI
```

Each contract must define API shape, authentication/security expectations, capability semantics, versioning, errors, timeouts, retries/idempotency where relevant, and compatibility policy.

## Consequences

### Positive

- AI infrastructure is implemented once and reused across the ecosystem.
- Provider routing and fallback can become consistent.
- AI memory and knowledge have a clear platform owner.
- Applications remain focused on business logic.
- Yasin-Agent can focus on agent execution rather than becoming an AI provider platform.
- YasinHub can operate Yasin-AI without owning its internals.
- Future AI capabilities can be added centrally and exposed to multiple projects.

### Negative / migration cost

- Existing local AI integrations in Relay, Feed, and Press cannot be removed immediately.
- Public AI contracts must be designed and versioned carefully.
- Yasin-AI becomes a critical shared platform and therefore requires stronger availability, observability, compatibility, and security discipline.
- Some functionality may need to move from application repositories into Yasin-AI over time.

## Non-Goals

This ADR does not:

- make Yasin-AI a dependency of every project immediately;
- require Yasin-AI to import Yasin-Core;
- move application business logic into Yasin-AI;
- introduce a shared database;
- introduce a global event bus;
- define the first AI API/SDK version.

Those are separate implementation or architecture decisions.

## Migration Direction

The ecosystem should converge in this order:

```text
1. Define AI capability catalog
2. Define v1 AI Capability Contract
3. Implement contract in Yasin-AI
4. Add YasinHub operational integration
5. Add YasinCLI adapter
6. Migrate Yasin-Agent
7. Migrate Relay / Feed / Press incrementally
8. Remove duplicated provider infrastructure only after compatibility is proven
```

## Compatibility Rule

Until a migration is complete, existing local AI/provider adapters remain supported. New cross-project AI infrastructure should be implemented in Yasin-AI unless an ADR explicitly grants an exception.

## Related Documents

- `docs/architecture/YASIN_ECOSYSTEM_CANONICAL_ARCHITECTURE_V1.md`
- `docs/architecture/ECOSYSTEM_DEPENDENCY_MATRIX_V1.md`
