# Yasin Ecosystem — Repository Inventory and Scope Lock

**Audit date:** 2026-08-09  
**Purpose:** prevent undocumented Yasin repositories from being omitted from architecture work.

## Primary Ecosystem

| Repository | Classification | Current architectural role | Audit status |
|---|---|---|---|
| Yasin-core | Core | Foundation/runtime | Audited baseline |
| Yasin-agent | Core | Agent platform/runtime | Audited baseline |
| Yasin-AI | Core | Modular AI platform | Audited baseline |
| YasinHub | Core | Management, registry, health, dashboard, integration | Audited baseline |
| YasinRelay | Core | Relay/content pipeline/integration | Audited baseline |
| Yasinfeed | Core | Feed/content generation and publishing | Audited baseline |
| Yasinpress | Core/Application | News collection and publishing | Audited baseline |
| Yasin-cli | Core/Control Plane | Ecosystem CLI, adapters, lifecycle/orchestration | Audited baseline |

## Supporting / Related

| Repository | Classification | Current evidence-based interpretation | Audit status |
|---|---|---|---|
| Openfeed | Supporting | Telegram public-feed/fetching/API/PWA project | Architecture record |
| Feedbridge | Supporting | Telegram bridge with vendored fetcher | Architecture record |
| TJC | Developer Tooling | Jules workflow/automation CLI | Architecture record |
| Termux-BackupManager | Operations | Termux backup/restore tooling | Architecture record |
| YasinCoder | Ecosystem Tooling Candidate | Yasin-named repository; role requires direct source audit | Scope candidate |
| YasinJules | Ecosystem Tooling Candidate | Yasin-named Jules-related repository; role requires direct source audit | Scope candidate |
| Telegram-Mirror | Related Candidate | Telegram-related repository; relationship to Yasin applications not yet verified | Scope candidate |
| YasinPress-Rewrite- | Private | Active rewrite of legacy YasinPress; has real packaging/tests/CI, but CI is currently **failing** on `main` — see `docs/projects/yasinpress-rewrite.md` for the specific failures found (2026-08-12 audit) | Audited, unstable |

## Explicitly Not Automatically Classified as Yasin Components

The owner account also contains repositories such as `bpb-worker-panel`, `Nova-Proxy`, `hermes-webui`, and `hermes-agent-mobile`. Their names alone do not establish membership in the Yasin architecture, so they are not promoted into the primary ecosystem without evidence.

## Scope Rule

Repository discovery is broader than the original project list. Any repository whose name, documentation, imports, configuration, or operational role establishes a Yasin ecosystem relationship must receive an architecture record before Phase 5 can be considered fully closed.

A repository may remain a `Scope candidate` when the available evidence is insufficient. This is preferable to silently omitting it or inventing a role.

## Important Discovery Result

The current GitHub account inventory revealed additional Yasin-named repositories that were not present in the original registry. They are therefore explicitly recorded here so future phases cannot accidentally forget them.
