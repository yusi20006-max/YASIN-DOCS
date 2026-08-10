# YasinFeed — Project Knowledge Pack

## Identity
- Repository: `yusi20006-max/YasinFeed`
- Role: general-purpose content aggregation, processing, rewriting, storage, scheduling, and publishing platform.

## Pipeline
```text
Sources
 ↓
Fetch
 ↓
Normalize / Models
 ↓
Rewrite / Summarize / Translate
 ↓
Storage
 ↓
Publish
 ├─ RSS
 ├─ PWA/API JSON
 └─ Eitaa
```

## Owns
- Feed/source fetching
- Content processing
- Rewrite/summary/translation adapters
- Storage
- Scheduling
- Publishing adapters
- API/PWA publishing surface
- Application-level security/configuration

## Does Not Own
- Ecosystem-wide lifecycle orchestration
- Agent execution platform
- Core runtime foundations
- Hub internals

## AI Boundary
Feed has provider-specific AI/rewrite extension points. A direct runtime dependency on Yasin-AI is not established by the current architecture audit.

## Storage
Feed owns application storage. It should not be treated as a shared ecosystem database.

## Relationship to YasinPress
Feed is general-purpose; Press is specialized Persian-news automation. Their overlapping RSS/content capabilities are an identified future refactoring opportunity, not a current dependency.

## Operational Boundary
```text
YasinCLI / YasinHub
          ↓ lifecycle
       YasinFeed
          ↓
    Content Pipeline
```

## Change Rules
Keep fetch, process, storage, and publishing boundaries explicit. New AI providers should enter through adapters. Changes that make Feed a shared foundation for Press require an ADR and dependency-matrix update.

## AI Agent Brief
For general feed aggregation/publishing behavior, inspect Feed first. Do not assume Feed and Press are interchangeable and do not introduce Yasin-AI coupling without a formal integration contract.
