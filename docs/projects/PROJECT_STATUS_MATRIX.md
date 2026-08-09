# Yasin Project Status Matrix

This matrix is intentionally conservative. `Partial` means the repository and a high-level role are known, not that the full architecture has been verified.

| Project | Repository Found | High-Level Role | Source Audit | Dependencies Verified | API Audit | CI/Test Audit |
|---|---:|---|---:|---:|---:|---:|
| Yasin-Core | Yes | Foundation/runtime | Partial | No | No | No |
| Yasin-Agent | Yes | Agent platform/runtime | Partial | No | No | No |
| Yasin-AI | Yes | AI component | Partial | No | No | No |
| YasinHub | Yes | Management/status | Partial | No | No | No |
| YasinRelay | Yes | Relay/integration | Partial | No | No | No |
| YasinFeed | Yes | Content generation/publishing | Partial | No | No | No |
| YasinPress | Yes | News collection/publishing | Partial | No | No | No |
| YasinCLI | Yes | Ecosystem control-plane CLI | Partial | No | No | No |
| YASIN-DOCS | Yes | Documentation hub | Yes | N/A | N/A | Partial |
| OpenFeed | Yes | Telegram fetching/API/PWA | Partial | No | No | No |
| FeedBridge | Yes | Telegram bridge/publishing | Partial | No | No | No |
| TJC | Yes | Jules automation CLI | Partial | No | No | No |
| Termux Backup Manager | Yes | Backup/restore tooling | Partial | No | No | No |

## Interpretation

This file is not a quality scorecard. It records **documentation evidence coverage**.

A `No` means the corresponding architecture fact has not yet been verified sufficiently to be treated as a central ecosystem fact.

## Completion Criteria

A project becomes fully audited when its record covers:

- source tree and module boundaries;
- runtime entry points;
- public APIs and contracts;
- configuration and secrets;
- dependencies and consumers;
- storage and data model;
- tests and CI/CD;
- issues and roadmap;
- external integrations;
- security boundaries;
- operational lifecycle;
- cross-project impact.
