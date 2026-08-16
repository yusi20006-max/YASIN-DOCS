# FINAL-01 — Ecosystem Remaining-Work Control Plane

**Issue:** YASIN-DOCS #14  
**Date:** 2026-08-16  
**Status:** ACTIVE (execution index)  
**Baseline preserved:** Yasin-AI **v1.1.4** public contracts; Quality Infrastructure (#10/#11/#12) merged

This document is the **canonical execution index**. No work is authorized outside a listed owning Issue. Duplicate/stale roadmap Issues are dispositioned here so implementers do not re-open product umbrellas as if they were defects.

---

## 1. Execution order (hard)

```text
PHASE A — Repository reconciliation (one repo at a time)
  1. Yasin-core     → #97 (owns disposition of #55 #56 #85)
  2. Yasinfeed      → #54 then #55 (owns disposition of #39 #45 #46)
  3. YasinPress-Rewrite- → #115 (owns disposition of #96)
  4. Yasin-cli      → #35 (owns disposition of open integration/audit Issues;
                         #34 BLOCKED-EXTERNAL until Settings)
  5. YasinHub       → #43 (owns disposition of #30 #31 #36 #38 #41)
  6. Yasin-agent    → #20 (#19 remains DEFERRED)

PHASE B — Cross-repository verification (YASIN-DOCS only)
  7. #15 FINAL-02 Cross-repo E2E harness activation
  8. #16 FINAL-03 Security / dependency / deployment gate
  9. #17 FINAL-11 Centralized contract CI activation

PHASE C — Final certification
 10. #18 FINAL-12 Final Ecosystem Certification (last gate)
```

**Rule:** In each batch, work **one repository only**. Complete merge + close + main verify before the next repository.

---

## 2. Inventory by repository

### 2.1 YASIN-DOCS

| Issue | Title | Priority | Disposition |
|-------|--------|----------|-------------|
| **#14** | FINAL-01 Control Plane | P0 | **THIS DOC** — docs only |
| **#15** | FINAL-02 Cross-repo E2E | P1 | Executable after Phase A |
| **#16** | FINAL-03 Security/Deploy gate | P1 | Executable after Phase A |
| **#17** | FINAL-11 Contract CI activation | P2 | Executable after #10 tooling on main |
| **#18** | FINAL-12 Certification | P0 final | **Last gate** — depends on all above |
| #10 #11 #12 | Quality infra | — | **CLOSED** (merged PR #13) |

### 2.2 Yasin-core

| Issue | Title | Disposition |
|-------|--------|-------------|
| **#97** | FINAL-04 Reconcile Core Roadmap | **OWNING** executable Issue |
| #55 | v3.3 Production Hardening | Subsumed by #97 — verify evidence, close if already met |
| #56 | v3.0 Stable Release | **STALE** — current version is **v3.3.0**; supersede under #97 |
| #85 | Architecture Boundary Lock | Docs-only; complete under #97 if gaps remain, else close with evidence |

**Current evidence:** `pyproject.toml` / README → **v3.3.0**, release-freeze validation in progress.

### 2.3 Yasinfeed

| Issue | Title | Disposition |
|-------|--------|-------------|
| **#54** | FINAL-05 Feed Production Hardening | **OWNING** executable |
| **#55** | FINAL-06 Feed Ecosystem Integration | **OWNING** after #54 |
| #39 | Production Hardening umbrella | Subsumed by #54 — do not expand scope beyond #54 AC |
| #45 | Ecosystem Integration Layer | Subsumed by #55 |
| #46 | v1.0 Production Release | Release meta — close only when #54+#55 AC met |

### 2.4 YasinPress-Rewrite-

| Issue | Title | Disposition |
|-------|--------|-------------|
| **#115** | FINAL-07 Persistence/Reporting/Runtime | **OWNING** executable |
| #96 | Phase 4 Persistence/Reporting/Runtime | Subsumed by #115 |

### 2.5 Yasin-cli

| Issue | Title | Disposition |
|-------|--------|-------------|
| **#35** | FINAL-08 CLI Current-State Reconciliation | **OWNING** executable |
| **#34** | Set default branch to main | **BLOCKED-EXTERNAL** (GitHub Settings / maintainer) |
| #1–#15, #27, #32 | Bootstrap / integration / audit umbrellas | Reconcile under #35; close obsolete if already implemented; **do not** expand into new product commands without AC |

### 2.6 YasinHub

| Issue | Title | Disposition |
|-------|--------|-------------|
| **#43** | FINAL-09 Hub Status-Plane Hardening | **OWNING** executable |
| #30 #31 #36 #38 #41 | Feed/Relay/Dashboard/Integration umbrellas | Subsumed by #43; Hub remains **status-plane**, not full control plane |

### 2.7 Yasin-agent

| Issue | Title | Disposition |
|-------|--------|-------------|
| **#20** | FINAL-10 Agent Production Readiness | **OWNING** executable (contract boundary verify) |
| **#19** | Integrate Yasin-AI contracts | **DEFERRED** — do not implement until explicitly activated |

### 2.8 Yasin-AI / YasinRelay

| Repo | Open issues | Disposition |
|------|-------------|-------------|
| Yasin-AI | **0 open** | Verification only; no feature work without new Issue |
| YasinRelay | **0 open** | Verification only; adapters already merged |

---

## 3. Status vocabulary (mandatory)

| Label | Meaning |
|-------|---------|
| **IMPLEMENTED** | Code + tests + evidence on main |
| **EXECUTABLE** | Open Issue with clear AC; work authorized |
| **SUBSUMED** | Covered by a FINAL-* owning Issue; close after parent evidence |
| **STALE** | Version/roadmap superseded; close with pointer |
| **DEFERRED** | Explicitly postponed (e.g. Agent #19) |
| **BLOCKED-EXTERNAL** | Requires Settings/human/ops outside CI (e.g. CLI #34) |
| **PLANNED** | Product idea without executable AC — **not authorized** |

---

## 4. Dependency graph

```text
#14 (control plane)
  └─► Phase A repos (independent of each other for implementation;
        certification depends on all)
        Core #97
        Feed #54 → #55
        Press #115
        CLI #35  (|| #34 external)
        Hub #43
        Agent #20  (#19 deferred)
  └─► Phase B (after Phase A complete)
        #15 E2E harness
        #16 Security/deploy
        #17 Contract CI activation
  └─► Phase C
        #18 Final certification
```

Cross-repo constraints (always):
- Consumers use **only** `yasinai.contracts` / `yasinai.services` / `yasinai.providers`.
- Forbidden: `knowledge_platform`, `security_platform`, `developer_platform`, private `yasinai.*`.
- Quality tooling already on main: `tools/contract_boundary`, `tools/architecture_boundary`, `tools/integration_harness`.

---

## 5. Explicitly NOT authorized without new Issue

- HA / distributed failover
- Untrusted plugin sandbox
- Advanced intelligent provider routing
- Live paid-provider E2E
- Agent #19 activation
- CLI default-branch Settings flip (#34) by automation
- New product features outside FINAL-* AC

---

## 6. Final certification prerequisites (#18)

All of the following must be true before #18 may declare readiness:

1. Phase A owning Issues closed with evidence on each repo `main`.
2. Phase B #15 #16 #17 closed or explicitly dispositioned with evidence.
3. CLI #34 either resolved or recorded BLOCKED-EXTERNAL with impact stated.
4. Agent #19 remains DEFERRED unless activated and completed.
5. No unresolved P0/P1 defect on the controlled integration path.
6. Implemented vs Deferred vs Planned matrix is truthful.

---

## 7. Acceptance (#14)

| Criterion | Met by this document |
|-----------|----------------------|
| Every remaining executable task has exactly one owning Issue | §2 FINAL-* owners |
| Duplicate/stale roadmap Issues identified | SUBSUMED / STALE rows |
| Dependencies and execution order documented | §1 §4 |
| Final certification has explicit prerequisites | §6 |
| No work authorized outside an Issue | §5 + ISSUE-ONLY rule |

**No production code changed under #14.**
