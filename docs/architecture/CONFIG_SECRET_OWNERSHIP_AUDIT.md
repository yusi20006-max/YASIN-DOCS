# Yasin Ecosystem — Configuration & Secret Ownership Audit

**Phase:** 6 — System Graphs  
**Status:** Consolidated baseline

## Ownership Model

Configuration and credentials belong to the runtime that consumes them. A repository may document a variable without owning the underlying external service.

```text
Configuration source
      ↓
Runtime configuration loader
      ↓
Validation
      ↓
Component
      ↓
External service / local resource
```

## Verified Examples

### YasinRelay

The documented environment contract includes Eitaa credentials, source channels, SQLite database path, logging/scheduling settings, and AI provider configuration such as provider, API key, base URL, and model.

The repository provides `.env.example` as the template boundary.

### Yasin-AI

The project documents explicit configuration/lifecycle management and a production deployment baseline. Plugin execution is trusted and in-process; untrusted remote plugin execution is explicitly outside the current security boundary.

### YasinHub

The current documented status system is file-backed and primarily records runtime status. It should not be treated as a secret manager.

## Secret Classes

```text
AI provider credentials
Publishing credentials
Messaging/bot credentials
GitHub/Jules credentials
Deployment credentials
External API credentials
```

These are classes, not claims that every component uses every class.

## Rules

1. Never commit real secrets.
2. Never duplicate a credential into another project's configuration without an explicit need.
3. Prefer least-privilege credentials per runtime.
4. Keep secret names separate from secret values in documentation.
5. Do not document real tokens, passwords, private keys, or session cookies.
6. Configuration examples must use placeholders.
7. A configuration variable is not automatically a public API contract.
8. Rotating a credential may require coordinated runtime restart and should be documented operationally.

## Verification Matrix

| Area | Current confidence | Next evidence |
|---|---|---|
| Relay environment contract | High | source/config cross-check |
| AI configuration boundary | Medium/High | source-level config loader |
| Hub status configuration | Medium | source-level config review |
| Core configuration | Medium | config package/source audit |
| Agent configuration | Medium | source-level loader audit |
| Feed configuration | Medium | `.env`/config/source audit |
| Press configuration | Medium | config/source audit |
| Secret rotation | Unknown | deployment/operations evidence |
| Central secret manager | Not established | deployment evidence |

## AI Maintainer Rule

When changing configuration, update the example/template, validation, documentation, tests, and migration notes together. Never silently rename a configuration key used by another runtime.
