# Yasin Ecosystem — Contract Registry v1

Canonical registry of audited ecosystem contracts.

## Status
- VERIFIED: source-level evidence exists.
- DOCUMENTED: repository documentation establishes the boundary.
- PLANNED: intended architecture only.
- NOT CONFIRMED: insufficient evidence for a dependency claim.

## Core
| ID | Owner | Contract | Status |
|---|---|---|---|
| CORE-SDK | Yasin-Core | Public `yasin_core.sdk` | VERIFIED |
| CORE-CLIENT | Yasin-Core | `YasinCoreClient` lifecycle | VERIFIED |
| CORE-AGENTS | Yasin-Core | Agent/runtime API | VERIFIED |
| CORE-TASKS | Yasin-Core | Task/job execution | VERIFIED |
| CORE-MEMORY | Yasin-Core | Memory API | VERIFIED |
| CORE-PROVIDER | Yasin-Core | Provider abstraction | VERIFIED |
| CORE-API | Yasin-Core | API gateway | VERIFIED |
| CORE-SECURITY | Yasin-Core | Security/RBAC | VERIFIED |
| CORE-COMPAT | Yasin-Core | Ecosystem compatibility | VERIFIED |

## Agent / Hub
| ID | Owner | Contract | Status |
|---|---|---|---|
| AGENT-CORE | Yasin-Agent | Core SDK integration | VERIFIED |
| AGENT-RUNTIME | Yasin-Agent | Agent runtime | VERIFIED |
| HUB-CORE | YasinHub | Core integration | VERIFIED |
| HUB-COMPAT | YasinHub | Compatibility integration | VERIFIED |
| HUB-ORCHESTRATION | YasinHub | Ecosystem orchestration | DOCUMENTED |

## Relay
| ID | Owner | Contract | Status |
|---|---|---|---|
| RELAY-AI-PROCESSOR | YasinRelay | `ContentProcessor` / `AIProcessor` | VERIFIED |
| RELAY-PIPELINE | YasinRelay | PipelineContext/stages | VERIFIED |
| RELAY-DEDUPE | YasinRelay | Content deduplication | VERIFIED |
| RELAY-MEDIA | YasinRelay | Media processing | DOCUMENTED |
| RELAY-PUBLISHER | YasinRelay | Eitaa publishing | VERIFIED |
| RELAY-EVENTS | YasinRelay | Pipeline events | VERIFIED |

## Feed / Press
| ID | Owner | Contract | Status |
|---|---|---|---|
| FEED-FETCH | YasinFeed | Feed collection | DOCUMENTED |
| FEED-REWRITE | YasinFeed | AI/rewrite boundary | DOCUMENTED |
| FEED-STORAGE | YasinFeed | Local persistence | DOCUMENTED |
| FEED-SCHEDULER | YasinFeed | Scheduling | DOCUMENTED |
| FEED-PUBLISHER | YasinFeed | Publishing | DOCUMENTED |
| PRESS-RSS-COLLECTOR | YasinPress | RSS collection | DOCUMENTED |
| PRESS-DEDUPE | YasinPress | Duplicate detection | DOCUMENTED |
| PRESS-CATEGORY | YasinPress | Categorization | DOCUMENTED |
| PRESS-AI | YasinPress | Optional AI | DOCUMENTED |
| PRESS-PUBLISH-QUEUE | YasinPress | Persistent queue | DOCUMENTED |
| PRESS-EITAA-PUBLISHER | YasinPress | Eitaa publishing | DOCUMENTED |
| PRESS-STORAGE | YasinPress | SQLite storage | DOCUMENTED |

## Yasin-AI
| ID | Owner | Contract | Status |
|---|---|---|---|
| AI-RUNTIME | Yasin-AI | Runtime platform | DOCUMENTED |
| AI-SERVICE | Yasin-AI | API/service layer | DOCUMENTED |
| AI-KNOWLEDGE | Yasin-AI | Knowledge/retrieval | DOCUMENTED |
| AI-MEMORY | Yasin-AI | Platform memory | DOCUMENTED |
| AI-PLUGIN | Yasin-AI | Plugin boundary | DOCUMENTED |
| AI-OBSERVABILITY | Yasin-AI | Instrumentation | DOCUMENTED |
| AI-PERSISTENCE | Yasin-AI | Persistence | DOCUMENTED |
| AI-DEPLOYMENT | Yasin-AI | Deployment boundary | DOCUMENTED |

## CLI
| ID | Owner | Contract | Status |
|---|---|---|---|
| CLI-CONTROL | YasinCLI | Unified control | PLANNED |
| CLI-STATUS | YasinCLI | `status` | PLANNED |
| CLI-DOCTOR | YasinCLI | `doctor` | PLANNED |
| CLI-LIFECYCLE | YasinCLI | `start/stop/restart` | PLANNED |
| CLI-ADAPTERS | YasinCLI | Project adapters | PLANNED |

## Dependency Claims
| Consumer | Dependency | Status |
|---|---|---|
| Yasin-Agent | Yasin-Core SDK | VERIFIED |
| YasinHub | Yasin-Core SDK | VERIFIED |
| YasinRelay | Yasin-AI | NOT CONFIRMED |
| YasinFeed | Yasin-AI | NOT CONFIRMED |
| YasinPress | Cloudflare Workers AI | DOCUMENTED |
| YasinPress | Yasin-AI | NOT CONFIRMED |
| Yasin-AI | Yasin-Core | NOT CONFIRMED |
| YasinCLI | Core/Agent/Hub/Relay | PLANNED |

## Governance
1. Every contract has one canonical owner.
2. Consumers use public APIs/adapters, not private implementation modules.
3. Local persistence is not shared memory by default.
4. Provider abstraction does not imply a dependency on another Yasin project.
5. New cross-project dependencies require source evidence or an explicit integration contract.
6. Breaking contract changes require an ADR.
7. Contract IDs remain stable; contract versions are separate from repository releases.

## Change Flow
```text
Implementation → Tests → Registry → Compatibility → ADR if needed → Release
```

**Status: Contract Registry v1 — consolidated canonical baseline complete.**
