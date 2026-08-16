# Pipeline ownership (post Phase-0)

See also: `ECOSYSTEM_POST_PHASE0_CERTIFICATION.md` §4.

## Principle

Independent domain products may implement collect → process → publish.
Shared AI capability is owned by **Yasin-AI** public contracts only.

| Pipeline stage | Relay | Feed | Press |
|----------------|-------|------|-------|
| Collect | OpenFeed/Telegram fetch | Multi-source fetch | RSS/sources |
| AI process | Yasin-AI adapter (or legacy) | YasinAIProvider (or legacy) | CF or yasinai |
| Publish | Eitaa | Eitaa/PWA/RSS | Eitaa |

Do not merge these orchestrators into Yasin-AI.
