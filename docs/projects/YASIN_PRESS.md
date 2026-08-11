# YasinPress — Project Knowledge Pack

## Identity
- Repository: `yusi20006-max/Yasinpress` (legacy, flat-script structure, no tests/CI)
- **Active rewrite: `yusi20006-max/YasinPress-Rewrite-`** (separate repo — see `docs/projects/yasinpress-rewrite.md` for source-verified detail, including current CI status). This is the actively developed codebase; the identity/pipeline description below applies conceptually to both, but only the rewrite has verified packaging, tests, and CI.
- Role: specialized Persian-news automation and Eitaa publishing application.

## Pipeline
```text
RSS Sources
 ↓
Collection
 ↓
Duplicate Detection
 ↓
Age / Priority / Category
 ↓
Optional AI Enrichment
 ↓
News Builder / Formatter / Hashtags / Digest
 ↓
Durable Queue
 ↓
Rate Limiter
 ↓
Eitaa
```

## Owns
- Persian news collection
- Duplicate and stale-news handling
- Categorization/prioritization
- Optional AI enrichment
- News formatting and hashtag generation
- Daily digest generation
- Durable publication queue
- Rate-limited Eitaa publishing
- Application-local state

## AI Boundary
Current architecture documents optional Cloudflare Workers AI with a rule-based fallback. A direct dependency on Yasin-AI is not established.

## Relationship to YasinFeed
Press is specialized for Persian news/Eitaa; Feed is general-purpose. Their overlap is an identified architectural opportunity, not a current dependency.

## Storage
Press owns its application state. It is not an ecosystem-wide database.

## Operational Boundary
```text
YasinCLI / YasinHub
          ↓ lifecycle
       YasinPress
          ↓
    News Pipeline
```

## Change Rules
Changes to queue semantics, publisher contracts, AI provider integration, news classification, or storage schema require compatibility and architecture review. Turning Feed into a shared foundation for Press requires an ADR.

## AI Agent Brief
For Persian news automation and Eitaa publishing, inspect Press first. Preserve its specialized pipeline. Do not merge it into Feed merely because both process RSS content.
