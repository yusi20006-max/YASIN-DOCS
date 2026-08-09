# ADR-0010: Feed, Content Generation, and Publishing Boundaries

- Status: Proposed
- Date: 2026-08-09
- Decision owners: Yasin ecosystem maintainers
- Scope: YasinFeed, YasinPress, relay/feed flows, and publishing integrations
- Supersedes: None
- Superseded by: None

## Context

The Yasin ecosystem includes feed ingestion, AI-assisted content generation/rewrite, and publication to downstream channels. Combining these responsibilities into one component would make ingestion, transformation, and delivery difficult to evolve independently.

## Decision

Feed ingestion, content generation/transformation, and publishing are treated as distinct responsibilities with explicit boundaries.

- **YasinRelay** owns relay/pipeline responsibilities within its defined scope.
- **YasinFeed** owns the news/content generation and publishing workflow defined for that project.
- **YasinPress** remains a distinct publishing/content application boundary where its documented responsibilities apply.
- Publishing integrations such as RSS, PWA, Eitaa, or other channels remain adapters/integration boundaries rather than becoming the owner of upstream content semantics.

No project should silently absorb another project's domain responsibility merely to simplify one workflow.

## Rationale

Separating ingestion, transformation, and delivery reduces coupling and allows each stage to be tested and evolved independently.

## Alternatives Considered

### One universal content service
Rejected because it would centralize unrelated concerns and increase coupling.

### Put publishing logic directly into every content producer
Rejected because channel-specific behavior would be duplicated and inconsistent.

## Consequences

### Positive

- Clear ownership of content stages.
- Reusable publishing adapters.
- Easier testing of generation versus delivery.
- Lower coupling between feed sources and publishing channels.

### Negative / Trade-offs

- Pipeline contracts must be explicit.
- Cross-project content changes require impact analysis.
- Publishing failures must be handled without corrupting upstream content state.

### Operational

Publishing should expose success/failure state and preserve enough information for retry or diagnosis where the implementation supports it.

### Security

Publishing credentials and channel-specific secrets belong to the publishing integration boundary and must not be embedded in content data or ADRs.

### Compatibility / Migration

Changes to content schemas or publishing contracts require consumer/adaptor analysis.

## Architecture Impact

Defines a conceptual flow:

```text
Sources / Feeds
      ↓
Ingestion / Relay
      ↓
Content Processing / Generation
      ↓
Publishing Adapters
      ↓
RSS / PWA / Eitaa / Other Channels
```

The exact runtime topology and ownership of individual stages must be verified against source repositories.

## Evidence

- `YASIN_AI_CONTEXT.md`
- `docs/architecture/`
- YasinFeed architecture documentation
- YasinRelay architecture documentation
- YasinPress architecture documentation

## Related Documents

- ADR-0001
- ADR-0005
- ADR-0007
- ADR-0009

## Open Questions

- Which content schema is the canonical cross-project contract?
- Which stages are synchronous versus asynchronous?
- Which publishing adapters guarantee retry/idempotency?
