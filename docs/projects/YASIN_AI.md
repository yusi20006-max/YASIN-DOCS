# Yasin-AI — Project Knowledge Pack

## Identity
- Repository: `yusi20006-max/Yasin-AI`
- Role: independent AI platform for modular runtime services, persistent memory, knowledge retrieval, developer extensions, API/service boundaries, observability, and secure deployment.
- README production release: `v1.1.0`.

## Owns
- AI runtime lifecycle
- Knowledge/retrieval components
- Persistent local memory
- Semantic/knowledge-oriented storage
- Plugin/developer extension contracts
- Transport-neutral service/API layer
- Observability primitives
- Production deployment/security baseline

## Does Not Currently Claim
- Distributed/high-availability storage
- Automatic multi-node failover
- Sandboxed untrusted remote plugin execution
- An automatically shared database for all Yasin applications

## Persistence
Default persistence is local SQLite-backed storage. This is Yasin-AI platform state and must remain conceptually distinct from application-local SQLite in Relay/Press.

## Security Boundary
Plugin execution is trusted and in-process. Untrusted remote plugin execution is not currently supported and requires a future sandbox/authorization layer.

## Ecosystem Position
Yasin-AI is treated as an independent platform boundary. A direct Yasin-AI → Yasin-Core dependency is not confirmed by the current architecture audit; do not invent one.

## Verification
README recommends:
```bash
python -m pytest -q
pip-audit
python -m build
```

## Versioning
Semantic versioning; immutable release tags; breaking changes require major versions.

## Change Rules
Changes to memory schema, service/API contracts, plugin contracts, deployment security, or persistence boundaries require compatibility/security review and relevant ADR updates.

## AI Agent Brief
If a task concerns AI platform runtime, knowledge, durable AI memory, plugins, AI service boundaries, or AI observability, inspect Yasin-AI first. Do not assume every application's AI adapter should import Yasin-AI directly. Introduce integrations through explicit contracts.
