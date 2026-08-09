# AI Change Impact Protocol

## Purpose

Determine what else may break before changing a Yasin component.

## Impact Levels

### L0 — Documentation only
No runtime contract changes.

### L1 — Internal implementation
Private behavior only; existing tests/contracts remain unchanged.

### L2 — Local public API
Changes a public symbol inside one repository.

### L3 — Cross-project contract
Changes an API, message, schema, configuration contract, lifecycle interface, or dependency consumed by another project.

### L4 — System architecture
Changes ownership, runtime topology, storage strategy, security boundary, deployment model, or core architectural assumptions.

## Impact Procedure

```text
Changed symbol/file
      ↓
Identify owner
      ↓
Find imports/consumers
      ↓
Find tests/fixtures/config
      ↓
Check public contract
      ↓
Check storage/message/config compatibility
      ↓
Classify impact
      ↓
Validate affected components
```

## Mandatory Checks

For L2+:

- public symbol compatibility;
- direct consumers;
- tests;
- configuration references;
- documentation references.

For L3+ additionally:

- producer/consumer contract;
- schema/versioning;
- backward compatibility;
- migration/rollout order;
- affected repositories.

For L4 additionally:

- architecture graph;
- security boundary;
- deployment implications;
- rollback strategy;
- ADR requirement.

## Change Order

When producer and consumer must change together, prefer:

```text
1. Introduce compatible producer behavior.
2. Update consumers.
3. Validate both.
4. Remove deprecated behavior only after compatibility window.
```

## AI Rule

Never assume a repository is isolated merely because the requested file is local. Search the documented dependency graph and source evidence before declaring impact L1.
