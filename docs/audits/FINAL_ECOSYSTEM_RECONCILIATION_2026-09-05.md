# Final Ecosystem Reconciliation — 2026-09-05

## Scope

This reconciliation aligns YASIN-DOCS with the final YasinHub ecosystem acceptance track (Issue #174) and records the current cross-project boundaries.

## Canonical boundaries

| Boundary | Owner |
|---|---|
| Ecosystem lifecycle / PID authority | YasinHub |
| Agent/workflow execution | Yasin-Agent |
| Shared AI capabilities/provider plane | Yasin-AI |
| Content relay/fetch/process/publish | YasinRelay |
| General content aggregation/publishing | YasinFeed |
| Persian news application | YasinPress-Rewrite- |
| MCP protocol/tool boundary | Yasin-MCP |
| Optional operations provider/gateway | Yasin-Operations |
| Cross-project architecture/docs | YASIN-DOCS |

## Acceptance evidence

- YasinHub: 478 passed
- Yasin-Agent: 240 passed
- YasinRelay: 108 passed
- Yasin-AI: 415 passed
- Real process/PID lifecycle: PASS
- PWA backend/API authority: PASS
- Security regression: PASS

## Outstanding acceptance items

- Real publish E2E remains operator-config dependent.
- PWA visual/mobile acceptance requires a real browser viewport.

These are not represented as completed in YASIN-DOCS.

## Governance

Future cross-project changes must update the affected project record, dependency/architecture documents and ADRs when a boundary or intentional architecture decision changes. Implementation evidence remains authoritative in each project repository; acceptance evidence remains in Yasin-Operations.
