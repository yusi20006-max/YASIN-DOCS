# Yasin Project Knowledge Pack — Index & Consistency Baseline

## Purpose

This index is the entry point for the project-specific knowledge packs in YASIN-DOCS. Each project pack describes the project's mission, ownership boundary, architecture, dependencies, storage, operational role, testing expectations, and rules for AI agents.

## Evidence Status

- **Confirmed**: supported by repository/source evidence.
- **Inferred**: strongly indicated but not fully source-verified.
- **Partial**: documentation exists but the repository audit is incomplete.
- **Open**: repository or implementation evidence is still required.

## Project Matrix

| Project | Role | Knowledge Pack | Audit Status | Canonical Dependency Notes |
|---|---|---|---|---|
| Yasin-Core | Runtime + SDK foundation | [YASIN_CORE.md](YASIN_CORE.md) | Confirmed baseline | Foundation; must not depend on higher-level apps |
| Yasin-Agent | Agent/workflow execution | [YASIN_AGENT.md](YASIN_AGENT.md) | Confirmed baseline | Agent → Core |
| Yasin-AI | AI platform | [YASIN_AI.md](YASIN_AI.md) | Confirmed baseline | Independent platform boundary; Core edge unresolved |
| YasinHub | Control + observability | [YASIN_HUB.md](YASIN_HUB.md) | Confirmed baseline | Hub → Core SDK / Agent SDK |
| YasinCLI | Unified CLI | [YASIN_CLI.md](YASIN_CLI.md) | Partial | First-class Core/Agent/Hub/Relay adapters documented; Feed/Press/AI remain open |
| YasinRelay | Content relay/publishing | [YASIN_RELAY.md](YASIN_RELAY.md) | Confirmed baseline | AIProcessor abstraction; not automatically Yasin-AI |
| YasinFeed | General content platform | [YASIN_FEED.md](YASIN_FEED.md) | Confirmed baseline | Provider adapters; no confirmed shared AI dependency |
| YasinPress | Persian news publishing | [YASIN_PRESS.md](YASIN_PRESS.md) | Confirmed baseline | Optional Cloudflare AI; distinct application boundary |

## Consistency Rules

1. Project packs must not contradict `docs/architecture/YASIN_ECOSYSTEM_CANONICAL_ARCHITECTURE_V1.md`.
2. A project pack may be more detailed than the canonical architecture but cannot create an unapproved cross-project dependency.
3. Implementation details must be marked as confirmed only when repository evidence supports them.
4. Similar functionality between projects is not evidence of dependency.
5. Operational control by YasinHub does not imply that a project imports Hub internals.
6. Application-local storage must not be described as shared ecosystem memory.
7. A provider adapter must not be described as a dependency on Yasin-AI unless an explicit integration contract exists.
8. Cross-project architectural changes require the relevant ADR and updates to the dependency matrix.

## AI Agent Reading Order

```text
PROJECT_KNOWLEDGE_PACK_INDEX.md
        ↓
YASIN_ECOSYSTEM_CANONICAL_ARCHITECTURE_V1.md
        ↓
ECOSYSTEM_DEPENDENCY_MATRIX_V1.md
        ↓
Target Project Knowledge Pack
        ↓
Target Repository README / Source / Tests
```

## Audit Gaps

### YasinCLI

The exact GitHub repository identity should be re-confirmed before the CLI knowledge pack is considered fully source-audited. Do not infer repository identity from naming alone.

### Cross-project contracts

The project packs describe current boundaries, but formal API/SDK payload schemas will be normalized during the API & Contract Registry phase.

### Version data

Version compatibility is intentionally deferred to the Compatibility Matrix phase. A project pack must not be treated as the authoritative compatibility table.

## Completion Criterion for Phase 6

Phase 6 is complete when:

- all project packs exist;
- every pack has the same conceptual sections;
- every dependency is classified as confirmed/inferred/open;
- the canonical architecture and project packs agree;
- unresolved repository identities are explicitly marked;
- the index provides a deterministic reading path for a new AI agent.

Current state: **Phase 6 knowledge-pack structure established; CLI repository verification and final cross-project consistency review remain open.**
