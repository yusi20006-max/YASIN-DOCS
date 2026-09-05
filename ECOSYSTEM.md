# Yasin Ecosystem

## Current canonical architecture

Yasin is a multi-repository ecosystem with explicit ownership boundaries. The verified operational path is:

```text
User / Operator
      ↓
YasinCLI / approved clients
      ↓
YasinHub — Control Plane
      ↓
Yasin-Core / Yasin-Agent / domain services
      ↓
Yasin-AI — shared AI capability plane
```

Content services include YasinRelay, YasinFeed and YasinPress. They retain domain ownership while consuming shared capabilities through public contracts.

## Control Plane rule

**YasinHub is the sole ecosystem lifecycle and PID authority.** Start, stop, restart, process identity, health and authoritative operational state belong to Hub. A PWA or client may request an operation but must not invent or persist an independent authoritative lifecycle state.

Yasin-Agent is the execution/runtime boundary; it is not a second Control Plane. Yasin-MCP owns MCP protocol/tool access. Yasin-Operations is an optional operations provider/gateway and does not replace Hub.

## AI boundary

**Yasin-AI is the canonical shared AI platform.** Provider routing, shared AI services and platform-owned AI capabilities belong there. Relay/Feed/Press/Agent must use explicit public/versioned contracts rather than private Yasin-AI imports or parallel ecosystem-wide AI infrastructure.

## Current evidence baseline — 2026-09-05

The final ecosystem acceptance track verified the software/runtime baseline on Android 11 API 30 ARM64 Termux:

- YasinHub: 478 tests passed
- Yasin-Agent: 240 tests passed
- YasinRelay: 108 tests passed
- Yasin-AI: 415 tests passed
- Real process/PID lifecycle and termination checks: passed
- PWA backend/API control authority: passed
- Security regression checks: passed

Overall acceptance remains **PARTIAL (FIXED), not FULL PASS**. The remaining blockers are external: valid operator publishing configuration for real publish E2E, and real-browser/mobile visual acceptance of the PWA.

## Source of truth

- Project repositories are authoritative for implementation.
- YASIN-DOCS is authoritative for cross-project architecture, boundaries, decisions and ecosystem guidance.
- Yasin-Operations is the canonical operational evidence/reporting repository for acceptance checkpoints.
- A target or proposed relationship must never be described as a confirmed runtime dependency without implementation evidence.
