# Yasin Ecosystem — AI Operating Rules

## Mission

Modify the smallest correct repository while preserving ecosystem contracts.

## Rules

1. Inspect before editing.
2. Identify ownership before changing behavior.
3. Prefer source evidence over assumptions.
4. Treat public APIs as contracts.
5. Treat storage and message schemas as compatibility boundaries.
6. Do not broaden scope without evidence.
7. Do not silently change configuration names.
8. Never commit secrets.
9. Run focused tests before broad tests.
10. Update architecture documentation when boundaries change.
11. Record unresolved uncertainty explicitly.
12. Never claim a test or verification was performed when it was not.

## Change Classification

```text
Documentation-only
Internal implementation
Public API
Cross-project contract
Schema/configuration
Runtime/deployment
Security-sensitive
```

The higher the classification, the broader the impact review.

## Dependency Rule

A dependency is considered confirmed only when source, package metadata, configuration, or explicit authoritative documentation supports it.

## API Rule

Do not expose an internal symbol merely because another component could technically import it. Public status requires an explicit contract or documented integration boundary.

## Schema Rule

Before changing a persistent or message schema, check existing consumers, migrations, compatibility, validation, fixtures, and rollback implications.

## Testing Rule

Test the changed behavior first. Then test direct consumers and relevant integration paths.

## Reporting Rule

Every completed task must state what changed, what was verified, what failed, and what remains uncertain.

## Stop Conditions

Pause and inspect more evidence when:

- ownership is ambiguous;
- an undocumented public dependency appears;
- a schema change affects unknown consumers;
- credentials or security boundaries are involved;
- deployment behavior is unclear;
- tests disagree with documented architecture.

## Golden Rule

**No silent architectural assumptions.**
