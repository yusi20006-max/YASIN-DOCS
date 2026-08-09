# Yasin Project Boundaries

This document defines the current high-level ownership boundaries. It intentionally avoids claiming unverified implementation details.

| Project | Owns | Does not automatically own |
|---|---|---|
| Yasin-Core | Foundation/runtime capabilities verified in its source | Application-specific workflows |
| Yasin-Agent | Agent platform/runtime behavior | Every AI provider capability |
| Yasin-AI | AI-related services/capabilities verified in its source | All agent orchestration |
| YasinHub | Management/status responsibilities verified in its source | Full runtime implementation |
| YasinCLI | User/developer control-plane CLI behavior | Business logic belonging to applications |
| YasinRelay | Relay/integration responsibilities verified in its source | All Telegram/news domain logic |
| OpenFeed | Telegram public-channel fetching/API/PWA scope | General content publishing policy |
| FeedBridge | Its bridge/publishing workflow | Core runtime or generic ecosystem management |
| YasinFeed | Content generation/publishing application workflow | Ecosystem-wide management |
| YasinPress | News collection/publishing application workflow | Generic runtime ownership |
| YASIN-DOCS | Ecosystem-level architecture and knowledge | Runtime execution |

## Boundary Rule

When a proposed change could reasonably belong to two projects, first identify the stable ownership boundary and existing contract. Do not duplicate functionality until the boundary has been reviewed.

## Known Boundary Investigations

The following require detailed source audit:

- Yasin-Core ↔ Yasin-Agent
- Yasin-Agent ↔ Yasin-AI
- YasinHub ↔ YasinCLI
- YasinRelay ↔ OpenFeed
- YasinRelay ↔ FeedBridge
- YasinFeed ↔ YasinPress

These are documented as investigation targets, not as evidence of a problem.
