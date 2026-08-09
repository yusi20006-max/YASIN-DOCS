# Phase 8 — Code Audit: Yasin-Core Pass 3

- Date: 2026-08-09
- Status: Evidence recorded
- Repository: `yusi20006-max/Yasin-core`
- Scope: concrete SDK client and service composition

## 1. Concrete SDK Dependency Direction

`YasinCoreClient` directly composes major Core services rather than acting as a thin HTTP wrapper. Its constructor imports and instantiates `AgentManager`, `TaskExecutor`, `AgentRuntime`, `ProviderManager`, `EventBus`, `PluginRegistry`, `ToolManager`, `RuntimeServiceRegistry`, `ContextEngine`, `DIContainer`, `ConfigurationManager`, storage, memory, orchestration, execution, security, observability, distributed workers, and compatibility services.

This establishes the SDK client as a **Core runtime composition root / facade**.

## 2. Agent Boundary Refinement

The concrete client creates both `AgentManager` and the official `AgentRuntime`, and exposes agent operations through SDK namespaces. Therefore Core owns the reusable lifecycle/runtime machinery for agents.

This strengthens the previous conclusion:

```text
Core = reusable runtime + agent/execution primitives
Agent = higher-level product/orchestration layer
```

The exact Yasin-Agent dependency direction still requires auditing that repository.

## 3. Provider Integration

`ProviderManager(client=self)` is instantiated by the Core client and registered in both DI and the runtime service registry. This makes provider management an explicit Core service.

The registry description identifies it as a unified AI provider abstraction layer. This confirms Core-side provider ownership at the runtime-infrastructure level.

It does not establish that Yasin-AI cannot provide higher-level provider routing, policy, knowledge, or application capabilities.

## 4. Storage and Memory

The client accepts an injectable storage backend, defaults to `InMemoryStorage`, initializes it, registers it in DI and the service registry, and can construct storage-backed long-term memory when persistent storage is supplied.

Therefore storage is not merely an independent utility; it participates directly in Core runtime composition and memory behavior.

## 5. Event and Service Registry

The client creates one EventBus and wires it into AgentManager, TaskExecutor, ContextEngine, and SecurityManager. It also registers services such as providers, observability, plugins, execution, storage, security, agent runtime, memory, API gateway, scheduler, and worker manager.

This establishes two important Core integration mechanisms:

- event-driven lifecycle/task signaling;
- service-registry/DI based composition.

## 6. Security and Compatibility

SecurityManager and CompatibilityManager are constructed and registered as first-class runtime services. Compatibility is therefore operationally integrated into the Core client rather than being documentation-only metadata.

## 7. Architecture Model

```text
                         YasinCoreClient
                         / Composition Root \
                                │
       ┌───────────────┬────────┼───────────────┐
       ↓               ↓        ↓               ↓
   Agent Runtime    Providers  Storage       Security
       │               │        │               │
       ↓               ↓        ↓               ↓
   Execution        AI infra  Memory        Authorization
       │
       └──────────────┬─────────────────────────┘
                      ↓
             EventBus + DI + ServiceRegistry
                      ↓
               External Consumers
```

## ADR Impact

| ADR | Result | Action |
|---|---|---|
| ADR-0002 | CONFIRMED | Core is a runtime composition/platform layer |
| ADR-0003 | PARTIAL | Must distinguish Core agent runtime from Yasin-Agent product orchestration |
| ADR-0007 | PARTIAL → stronger evidence | Core owns provider runtime infrastructure; higher-level Yasin-AI role remains to verify |
| ADR-0008 | PARTIAL → stronger evidence | Core storage is runtime-owned; ecosystem data ownership remains separate question |
| ADR-0009 | CONFIRMED | Security is an explicit runtime service |

## Important Caution

This pass inspected the concrete Core client, but not the implementation of every service it composes. Therefore no claim should yet be made about internal behavior of ProviderManager, CompatibilityManager, or storage backends beyond their observed composition and public role.

## Next Pass

Audit Yasin-Agent source-level imports, client initialization, Core SDK usage, runtime lifecycle, tools, memory, sessions, and workflow orchestration. Then produce the first concrete Core↔Agent dependency graph.
