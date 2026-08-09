# AI Security Protocol

## Purpose

Protect credentials, data, runtime boundaries, and external integrations while modifying Yasin.

## Non-Negotiable Rules

1. Never commit secrets, tokens, private keys, cookies, or real credentials.
2. Never print secret values in logs or task reports.
3. Use placeholders in examples.
4. Do not broaden permissions without an explicit requirement.
5. Treat external inputs as untrusted.
6. Validate data at trust boundaries.
7. Preserve authentication and authorization checks.
8. Do not disable security controls just to make tests pass.
9. Do not introduce remote execution or plugin loading without explicit review.
10. Record security-impacting architectural changes.

## Trust Boundary Review

For changes involving network, plugins, tools, credentials, storage, or user-controlled input, identify:

```text
Source
 ↓
Trust boundary
 ↓
Validation
 ↓
Authorization
 ↓
Execution
 ↓
Persistence / output
```

## Plugin Rule

A plugin system must not automatically be interpreted as a sandbox. If execution is trusted/in-process, document it as such and preserve that boundary unless a sandbox is deliberately designed and tested.

## Secret Handling

Documentation may name a secret variable such as `AI_API_KEY`; it must never contain the actual value.

## Security Changes

For security-sensitive changes, validate both positive and negative paths:

- authorized operation succeeds;
- unauthorized operation fails;
- malformed input is rejected;
- missing credentials fail safely;
- secrets do not leak into output/logs;
- least privilege remains intact.

## Incident Rule

If a secret is discovered in repository content, stop normal publication workflow, avoid copying it into documentation, rotate/revoke it through the appropriate owner, and document only the remediation—not the secret.
