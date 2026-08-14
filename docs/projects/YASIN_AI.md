# Yasin-AI — Project Knowledge Pack

## Identity
- Repository: `yusi20006-max/Yasin-AI`
- Role: Canonical AI capability platform for the Yasin ecosystem (ADR-001).
- Current release: **v1.1.1** (Phases 2–5 complete: contracts, providers, services, ecosystem integration, production hardening).

## Owns
- Public capability contracts (`yasinai.contracts` v1): memory, knowledge, embedding, plugin, generation, RAG
- Service facades (`yasinai.services`): KnowledgeService, GenerationService, RagService
- Provider boundary (`yasinai.providers`): ProviderBase, Registry, Router, OpenAI/Anthropic/Local adapters
- Ecosystem integration reference clients (`yasinai.integration`): Agent, Hub, CLI, Relay, Feed, Press
- AI runtime lifecycle, knowledge/retrieval, durable local memory
- Plugin/developer extension contracts (trusted in-process only)
- Transport-neutral service/API layer, observability primitives
- Production deployment/security baseline

## Consumer import rule
Consumers (Yasin-Agent, YasinHub, YasinCLI, YasinRelay, YasinFeed, YasinPress) **must** import from:
- `yasinai.contracts`
- `yasinai.services` and/or `yasinai.integration`

They **must not** import `knowledge_platform`, `developer_platform`, or provider SDKs directly.

## Does Not Currently Claim
- Distributed/high-availability storage
- Automatic multi-node failover
- Sandboxed untrusted remote plugin execution (see Plugin Trust Policy; planned toward v1.2.0)
- An automatically shared database for all Yasin applications

## Persistence
Default persistence is local SQLite-backed storage. Distinct from application-local SQLite in Relay/Press.

## Security Boundary
Plugin execution is trusted and in-process. `PluginRegistry` rejects `trusted=False` by default (`PluginTrustError`). Untrusted remote plugin execution is not supported.

## Provider credentials
Read only from environment (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`). Never committed.

## Ecosystem Position
Independent platform boundary per ADR-001 / ADR-0007. Integrations through explicit contracts.

## Verification
```bash
python -m pytest -q
pip-audit
python -m build
```

## Versioning
Semantic versioning; immutable release tags; breaking changes require major versions.

## Change Rules
Changes to memory schema, service/API contracts, plugin contracts, deployment security, or persistence boundaries require compatibility/security review and relevant ADR updates in YASIN-DOCS.

## AI Agent Brief
If a task concerns AI platform runtime, knowledge, durable AI memory, plugins, AI service boundaries, or AI observability, inspect Yasin-AI first. Introduce integrations through explicit contracts/services only.
