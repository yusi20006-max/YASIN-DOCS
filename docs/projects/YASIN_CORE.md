# Yasin-Core — Project Knowledge Pack

## Identity
- Repository: `yusi20006-max/Yasin-Core`
- Role: shared runtime, SDK, context, memory, execution, security, storage, compatibility, and observability foundation.
- Current repository version stated by README: `3.3.0`.
- Current status: release-freeze validation / production-readiness and documentation alignment.

## Owns
- Agent/runtime primitives
- Context and memory abstractions
- API gateway/integration surfaces
- Execution, workers, queues, scheduler
- SDK contracts
- Provider/plugin extension points
- Security, storage, observability
- Compatibility/migration foundations

## Does Not Own
- Product-specific news/content workflows
- Ecosystem-level operational policy
- Hub internals
- Press/Feed/Relay business logic

## Major Modules
`agents`, `api`, `compatibility`, `config`, `context`, `core`, `di`, `events`, `execution`, `memory`, `observability`, `plugins`, `providers`, `runtime`, `sdk`, `security`, `storage`.

## Ecosystem Position
```text
Yasin-Agent → Yasin-Core
YasinHub    → Yasin-Core SDK
YasinCLI    → Core adapter
```

## Key Boundaries
- Higher-level applications consume public contracts; they should not depend on Core internals.
- Core must remain below Hub and product-specific applications in dependency direction.
- Local Core memory/storage is not automatically ecosystem-wide shared memory.

## Validation
Typical test entry point: `pytest`. README states coverage across runtime, agents, API, compatibility, execution, scheduler, storage, SDK, observability, security, and integration.

## Important Source Notes
The README explicitly warns that historical documents may contain legacy cross-project references. Use current source and public interfaces as implementation authority.

## Change Rules
Changes to public SDK/runtime contracts require compatibility review and potentially an ADR plus ecosystem compatibility update.

## AI Agent Brief
If a task concerns generic runtime, SDK, execution, memory, context, provider, security, storage, or observability foundations, investigate Core first. Do not move application-specific behavior into Core simply to reuse code.
