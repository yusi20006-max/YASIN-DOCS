# Yasin-AI — Project Architecture Record

## Identity

- Repository: `yusi20006-max/Yasin-AI`
- Current release: `v1.1.0`
- Role: modular AI platform
- Documented state: production release with security/performance/reliability baseline

## Responsibility

Yasin-AI is organized around runtime orchestration, API/service boundaries, knowledge/retrieval, persistent memory, developer/plugin extensions, observability, and deployment/infrastructure.

## Architectural Areas

```text
Runtime orchestration
API / service layer
Knowledge / retrieval
Persistent memory
Developer / plugin platform
Observability
Deployment / infrastructure
```

## Persistence

The documented default persistence model is local SQLite-backed storage. The project explicitly does not claim distributed/high-availability storage or automatic multi-node failover.

## Security Boundary

Plugin execution is trusted and in-process. Untrusted remote plugin execution is explicitly not supported and would require a future sandbox/authorization layer.

## Verification

Documented release verification includes pytest, pip-audit and Python package build. Container deployments additionally verify production compose and healthcheck behavior.

## Ecosystem Boundary

Yasin-AI should be distinguished from Yasin-Agent: the repositories have overlapping agent/AI concepts, so ownership must be established from source-level interfaces rather than names alone.

## Audit Status

**Level 3:** high-level architecture, production posture and important security/storage boundaries are documented. Detailed source/API/dependency and cross-project contract audit remains required.
