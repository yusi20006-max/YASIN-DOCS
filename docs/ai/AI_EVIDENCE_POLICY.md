# Yasin Ecosystem — AI Evidence Policy

## Purpose

Prevent hallucinated architecture and distinguish facts from assumptions.

## Evidence Hierarchy

### Level 1 — Source verified

Code, package metadata, tests, configuration, migrations, or executable definitions directly establish the claim.

### Level 2 — Project documented

Official README/docs explicitly state the behavior but source verification is pending.

### Level 3 — Inferred

The claim follows logically from verified evidence but is not directly stated.

### Level 4 — Candidate

A plausible architectural possibility requiring verification.

### Level 5 — Unknown

There is not enough evidence to decide.

## Search Failure Rule

```text
No search result
    ≠
No implementation
```

Search/index limitations must not become architectural facts.

## Conflict Rule

If two sources conflict:

1. identify both;
2. prefer newer authoritative source/configuration where appropriate;
3. inspect code if implementation reality matters;
4. record the discrepancy;
5. do not silently choose a convenient interpretation.

## Documentation Rule

Every new architectural claim should be traceable to a repository, file, symbol, configuration entry, test, or explicit documented statement whenever practical.

## AI Output Rule

When uncertain, use language such as:

- verified;
- documented;
- inferred;
- candidate;
- unknown;
- requires source verification.

Never present a candidate as a fact.
