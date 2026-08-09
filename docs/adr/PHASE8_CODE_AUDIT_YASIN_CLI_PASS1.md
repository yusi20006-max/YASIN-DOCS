# Phase 8 — YasinCLI Code Audit Pass 1

- Date: 2026-08-09
- Repository: `yusi20006-max/Yasin-cli`
- Audited branch: `initial-setup`
- Status: Evidence recorded

## 1. Actual Role

YasinCLI is the intended **top-level unified user interface** for the Yasin ecosystem. Unlike YasinHub, which is an operational/control service, YasinCLI exposes one consistent command surface over multiple Yasin components.

The README describes it as a modular Node.js CLI targeting Termux/Android, Linux, macOS, and Windows.

## 2. Current Ecosystem Scope

The bootstrap creates ecosystem adapters for Yasin-Core, Yasin-Agent, YasinHub, and YasinRelay and registers dedicated commands for each. The CLI therefore already has a first-class ecosystem abstraction rather than a collection of unrelated shell wrappers.

## 3. Architecture

```text
User
  ↓
YasinCLI
  │
  ├── CommandRegistry
  ├── ConfigManager
  ├── Doctor
  ├── Status / Health / Logs
  ├── PluginSystem
  ├── ProfileManager
  └── EcosystemOrchestrator
          │
          ├── CoreAdapter
          ├── AgentAdapter
          ├── HubAdapter
          └── RelayAdapter
```

This is the correct conceptual position for YasinCLI: **presentation/control interface above ecosystem services**.

## 4. Orchestration Engine

`EcosystemOrchestrator` implements dependency-aware lifecycle ordering. For `start`, dependencies are resolved before dependents. For `stop`, the resulting order is reversed. Cycles are detected and rejected.

This makes YasinCLI an actual ecosystem lifecycle coordinator rather than merely a command multiplexer.

## 5. Adapter Boundary

The CLI isolates service-specific behavior behind adapters. The Core adapter is `library` mode, while Agent and Hub are currently represented as executable/one-shot integrations.

```text
CoreAdapter
  serviceId: yasin-core
  mode: library

AgentAdapter
  serviceId: yasin-agent
  mode: oneshot

HubAdapter
  serviceId: yasin-hub
  mode: oneshot
```

The adapter pattern prevents ecosystem-specific implementation details from leaking into the command layer.

## 6. Critical Hub Relationship

YasinHub already exposes an operational CLI/control plane. YasinCLI must therefore sit **above** Hub rather than compete with it.

```text
User
  ↓
YasinCLI                 ← unified UX
  ↓
Ecosystem adapters
  ↓
YasinHub                 ← operational control
  ↓
Core / Agent / Relay / ...
```

YasinCLI should delegate Hub-specific lifecycle/health behavior instead of reimplementing Hub internals.

## 7. Current Scope Gap

Yasin-AI is a first-class ecosystem project in the broader architecture, but the current `createEcosystemAdapters()` implementation only creates Core, Agent, Hub, and Relay adapters.

Therefore **Yasin-AI is currently absent from the CLI's first-class adapter graph**. YasinFeed and YasinPress are also absent from the inspected adapter factory and require explicit decisions before final ecosystem CLI architecture is accepted.

## 8. Dependency Graph

The orchestrator accepts an external `dependencies` configuration and resolves it dynamically. Lifecycle dependencies are therefore configuration-driven rather than hard-coded into the orchestrator.

```text
             YasinCLI
                 │
        ┌────────┴─────────┐
        ↓                  ↓
  Adapter Graph       Command Layer
        │
 ┌──────┼────────┬────────┐
 ↓      ↓        ↓        ↓
Core  Agent     Hub     Relay
```

## 9. ADR Impact

| Area | Result |
|---|---|
| CLI as unified UX | **CONFIRMED** |
| CLI as ecosystem orchestrator | **CONFIRMED** |
| Adapter architecture | **CONFIRMED** |
| Dependency-aware lifecycle | **CONFIRMED** |
| Hub below CLI | **CONFIRMED AS TARGET** |
| Yasin-AI CLI integration | **GAP IDENTIFIED** |
| Feed/Press CLI integration | **GAP IDENTIFIED** |
| CLI replacing Hub internals | **REJECTED** |

## 10. Next Step

Inspect remaining adapters, dependency configuration, lifecycle implementation, and tests. Then produce the first **Yasin-Core / Agent / AI / Hub / CLI dependency matrix**, including missing adapters and ownership boundaries.
