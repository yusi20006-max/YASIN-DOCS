# Phase 8 — Code Audit: Yasin-Core Pass 2

- Date: 2026-08-09
- Status: Evidence recorded
- Repository: `yusi20006-max/Yasin-core`
- Scope: public SDK, events, provider/storage/security exports

## 1. Public SDK Boundary

`yasin_core.sdk` explicitly exports `YasinCoreClient` and `AsyncYasinCoreClient`, plus public agent, context, tool, storage, execution, provider, security, observability, API, and compatibility surfaces.

This establishes a real public package boundary rather than a documentation-only concept.

## 2. SDK Contract

`ISDKClient` defines a minimal client contract containing `start()`, `stop()`, `health()`, and `status()`. `ISDKAuthenticator` defines client-side authentication header generation.

This confirms that external consumers have a formal SDK abstraction, although complete concrete client behavior still requires direct inspection.

## 3. Event Boundary

`yasin_core.events` publicly exports `Event` and `EventBus`, with lifecycle/task event constants for agent and task events. EventBus is therefore a concrete Core integration primitive.

## 4. Provider Boundary

The SDK exports `AIProvider`, request/response models, provider errors, `ProviderRegistry`, `ProviderManager`, and concrete `MockProvider`, `LocalProvider`, and `OpenAICompatibleProvider` implementations.

Yasin-Core definitely owns a provider abstraction/runtime layer. This does not by itself prove that Yasin-Core is the ecosystem-wide owner of every AI provider integration; Yasin-AI ownership still requires cross-repository verification.

## 5. Storage Boundary

The SDK exports `BaseStorage`, `JSONFileStorage`, `InMemoryStorage`, `get_storage`, and `register_backend`. Storage is therefore a first-class Core capability, while cross-project schema/data ownership remains unverified.

## 6. Security Boundary

The SDK exports authentication/authorization and security primitives including roles, permissions, policies, credential-store abstractions, audit logging, and `SecurityManager`. Security is a Core platform capability.

## 7. Compatibility Boundary

The SDK exports compatibility/version/migration facilities including validators for Agent, Hub, Relay, CLI, and Runtime compatibility. This is strong evidence that Core participates in ecosystem-wide compatibility contracts.

## Architecture Graph Update

```text
                    Yasin-Core Public SDK
                            │
      ┌─────────────┬───────┼────────┬─────────────┐
      ↓             ↓       ↓        ↓             ↓
   Agents        Events  Providers Storage      Security
      │             │       │        │             │
      └─────────────┴───────┼────────┴─────────────┘
                            ↓
                    External Consumers
                            │
             ┌──────────────┼──────────────┐
             ↓              ↓              ↓
          Agent           Hub            Relay
             │              │              │
             └──────────────┼──────────────┘
                            ↓
                     Compatibility Layer
```

This is an architectural evidence model, not proof that every consumer currently imports every capability.

## ADR Impact

| ADR | Result | Reason |
|---|---|---|
| ADR-0002 | CONFIRMED with stronger evidence | Public SDK and foundational services are explicit |
| ADR-0003 | PARTIAL | Core publicly exports agent runtime primitives |
| ADR-0007 | PARTIAL | Core owns provider abstractions; ecosystem-wide ownership remains unresolved |
| ADR-0008 | PARTIAL | Core owns storage abstractions; cross-project ownership remains unresolved |
| ADR-0009 | CONFIRMED with stronger evidence | Core exposes explicit auth/security primitives |

## Next Pass

Inspect concrete `YasinCoreClient`/`AsyncYasinCoreClient`, provider manager, storage backend registration, and compatibility validators, then inspect Yasin-Agent imports and configuration to establish actual dependency direction.
