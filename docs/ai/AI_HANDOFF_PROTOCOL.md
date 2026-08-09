# AI Handoff Protocol

## Purpose

Ensure another AI can continue work without reconstructing the previous agent's reasoning from scratch.

## Required Handoff

Every completed implementation task should provide:

```text
PROJECT
REPOSITORY
BRANCH
TASK / ISSUE

WHAT CHANGED
- files
- behavior
- contracts

VALIDATION
- tests run
- passed
- failed
- skipped

ARCHITECTURE IMPACT
- none / L0 / L1 / L2 / L3 / L4
- affected consumers
- docs updated

KNOWN LIMITATIONS
- unresolved issues
- unverified assumptions

NEXT STEP
- exact recommended continuation
```

## Evidence Requirement

Separate:

```text
Verified result
Inference
Unresolved uncertainty
```

Do not leave the next agent to guess whether a statement is a fact or an assumption.

## Interrupted Work

If work stops before completion, record:

- current branch;
- current commit;
- files modified;
- completed steps;
- incomplete steps;
- tests already run;
- known failures;
- exact next action.

## Cross-Agent Continuation

The next AI should first read the handoff, then inspect repository state and diff before continuing. It must not assume the previous agent's working tree is clean or that a claimed test actually passed.

## Completion Language

Use precise states:

- `COMPLETE` — implementation and required validation are done.
- `PARTIAL` — some required work remains.
- `BLOCKED` — external condition prevents progress.
- `FAILED` — attempted implementation/validation failed.
- `UNKNOWN` — insufficient evidence.

## Ecosystem-Level Handoff

For cross-project work, include all affected repositories and dependency order. If another repository must change before this one can safely deploy, state that explicitly.

## Golden Rule

**A handoff is a reproducibility artifact, not a status message.**
