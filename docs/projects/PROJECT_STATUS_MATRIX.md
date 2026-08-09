# Yasin Project Status Matrix

This matrix is intentionally conservative. `Partial` means the repository and a high-level role are known, not that the full architecture has been verified.

| Project | Repository Found | Architecture Record | Source/Manifest Audit | Dependencies Verified | API Audit | CI/Test Audit |
|---|---:|---:|---:|---:|---:|---:|
| Yasin-Core | Yes | Yes | Partial | Partial | Partial | No |
| Yasin-Agent | Yes | Yes | Partial | Partial | Partial | No |
| Yasin-AI | Yes | Yes | Partial | Partial | Partial | Partial |
| YasinHub | Yes | Yes | Partial | No | No | Partial |
| YasinRelay | Yes | Yes | Partial | No | No | No |
| YasinFeed | Yes | Yes | Partial | Partial | Partial | No |
| YasinPress | Yes | Yes | Partial | No | No | No |
| YasinCLI | Yes | Yes | Partial | No | Partial | Partial |
| YASIN-DOCS | Yes | Yes | Yes | N/A | N/A | Partial |
| OpenFeed | Yes | Yes | Partial | Partial | Partial | No |
| FeedBridge | Yes | Yes | Partial | Partial | Partial | No |
| TJC | Yes | Yes | Partial | Partial | Partial | Partial |
| Termux Backup Manager | Yes | Yes | Partial | Partial | Partial | No |

## Phase 5 Interpretation

The **Architecture Record** column means a project-level documentation record now exists. It does not mean the underlying implementation has been fully audited.

`Partial` in the source, dependency, API, or CI columns means there is repository-level evidence or documented implementation information, but the complete source-level contract has not yet been verified.

## Current Deep-Audit Evidence

`docs/projects/SOURCE_LEVEL_AUDIT.md` records the first implementation-manifest evidence pass across the ecosystem. It should be read together with the project-specific records.

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
