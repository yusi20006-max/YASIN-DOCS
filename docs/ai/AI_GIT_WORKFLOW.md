# AI Git Workflow

## Purpose

Provide a safe, repeatable Git workflow for AI agents modifying Yasin repositories.

## Standard Flow

```text
Inspect repository state
        ↓
Understand branch/base
        ↓
Create focused branch when required
        ↓
Inspect source + tests
        ↓
Implement bounded change
        ↓
Run validation
        ↓
Review diff/status
        ↓
Commit with precise message
        ↓
Push / PR according to project workflow
        ↓
Report result
```

## Before Editing

Check current branch, working-tree state, repository instructions, relevant issue/PR, and existing uncommitted work. Never overwrite unrelated user changes.

## Branch Rule

For repository work that will become a PR, use a focused descriptive branch. Do not mix unrelated fixes.

## Commit Rule

A commit should represent one coherent change. Commit messages should explain intent.

## Diff Review

Before completion inspect Git status, diff, changed files, tests, generated files, secrets, and unexpected formatting.

## PR Rule

A PR description should contain:

- Goal
- Repository
- Issue/task
- Requirements
- Implementation summary
- Tests/validation
- Architecture impact
- Known limitations
- Pre-merge checklist

## AI Safety

Do not force-push unless explicitly authorized; reset/discard user work without authorization; rewrite unrelated commits; commit secrets; claim CI passed without evidence; or merge merely because code looks correct.

## Multi-Repository Changes

Keep repository changes independently reviewable unless coordinated release requires otherwise. Record dependency order when multiple PRs must land together.

## Handoff

After publishing work, report exact branch/commit/PR references, tests, remaining failures, and whether downstream repositories need updates.
