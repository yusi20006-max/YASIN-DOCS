# Yasin Projects

This is the cross-project registry. Implementation claims require repository/source/runtime evidence.

## Core runtime and control architecture

| Repository | Canonical role | Current acceptance status |
|---|---|---|
| `Yasin-core` | Shared runtime/foundation layer | Core foundation |
| `Yasin-agent` | Agent/workflow execution | Final ecosystem regression: 240 passed |
| `Yasin-AI` | Canonical shared AI platform/provider boundary | Final ecosystem regression: 415 passed; Termux ARM64 compatibility blocker fixed |
| `YasinHub` | **Ecosystem Control Plane, lifecycle/PID authority and observability** | Final ecosystem regression: 478 passed |
| `Yasin-cli` | Unified user-facing CLI/orchestration | Existing repository; future audit remains separate |
| `YasinRelay` | Content relay/fetch/process/publish pipeline | Final ecosystem regression: 108 passed; real publish still operator-config dependent |
| `Yasinfeed` | Content aggregation/processing/publishing | Domain application |
| `YasinPress-Rewrite-` | Persian news collection/AI processing/publishing | Domain application |
| `YASIN-DOCS` | Canonical cross-project architecture/documentation | This repository |

## Supporting / optional

| Repository | Role | Boundary |
|---|---|---|
| `Yasin-MCP` | MCP protocol/tool access boundary | Does not own lifecycle |
| `Yasin-Operations` | Operations provider/gateway and evidence/reporting | Optional; does not replace YasinHub |
| `Openfeed` | Go public-channel fetcher/API/PWA | Fetching foundation |
| `Feedbridge` | Content bridge | Supporting/domain integration |
| `TJC` | Termux/Jules workflow tooling | Developer automation |
| `Termux-BackupManager` | Termux backup/restore tooling | Operations tooling |

## Canonical control flow

```text
User / Operator
      ↓
YasinCLI / approved clients
      ↓
YasinHub
      ↓
project runtimes
```

Hub owns ecosystem-level lifecycle coordination and authoritative PID/process state. Agent owns execution semantics; Relay/Feed/Press own content semantics; Yasin-AI owns shared AI capabilities.

## Canonical AI flow

```text
Agent / Relay / Feed / Press / future consumers
                     ↓
          public/versioned AI contract
                     ↓
                 Yasin-AI
```

Private module imports and duplicate ecosystem-wide provider infrastructure are not canonical.

## Final acceptance evidence — 2026-09-05

Issue #174 final acceptance on Android 11 API 30 ARM64 Termux recorded:

- Hub: 478/478 passed
- Agent: 240/240 passed
- Relay: 108/108 passed
- AI: 415/415 passed
- Real PID lifecycle/identity/termination: PASS
- PWA backend/API authority: PASS
- Security regression: PASS

Overall: **PARTIAL (FIXED)**. The remaining external blockers are real publish E2E operator configuration and real-browser/mobile visual PWA acceptance.

## Registry rule

Do not infer architectural membership from repository names. When registry text conflicts with implementation, record and reconcile the discrepancy using repository evidence. Detailed project records remain under `docs/projects/` and audit evidence remains in `Yasin-Operations`.
