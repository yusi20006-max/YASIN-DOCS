# Ecosystem Re-baseline — Phase 0

**Issue:** YASIN-DOCS #7  
**Date:** 2026-08-16  
**Status:** Complete (documentation baseline) + **P0/P1 execution closed** (see §14)  
**Authority rule:** Repository/code/test evidence overrides stale documentation.

---

## 1. Repositories Inspected

| # | Repository | Default branch | Evidence sources |
|---|---|---|---|
| 1 | `yusi20006-max/YASIN-DOCS` | `main` | ADR set, PROJECTS.md, audits |
| 2 | `yusi20006-max/Yasin-core` | `main` | README, pyproject, version.py |
| 3 | `yusi20006-max/Yasin-AI` | `main` | README, pyproject **v1.1.4**, PUBLIC_API_CONTRACT, tree |
| 4 | `yusi20006-max/Yasin-agent` | `main` | README, pyproject, agent_platform/__init__.py **v1.0.0** |
| 5 | `yusi20006-max/YasinHub` | `main` | README, package layout |
| 6 | `yusi20006-max/Yasin-cli` | `initial-setup` (main branch exists) | README (Node.js CLI) |
| 7 | `yusi20006-max/YasinRelay` | `main` | README **v2.0.0**, ai_processor.py, pipeline, hub_integration |
| 8 | `yusi20006-max/Yasinfeed` | `main` | README, yasinfeed/ai/*, engine |
| 9 | `yusi20006-max/YasinPress-Rewrite-` | `main` | README, pyproject **1.0.0**, yasinpress/ai/* |

**Canonical AI baseline (locked for this phase):** Yasin-AI **v1.1.4** (`pyproject.toml` + README).

---

## 2. Major Findings (Pre-Implementation)

1. **Yasin-AI v1.1.4 is the verified AI platform.** Public contracts exist under `yasinai.contracts`, `yasinai.services`, `yasinai.providers`. Private packages (`knowledge_platform`, `security_platform`, `developer_platform`) must not be imported by consumers.
2. **No consumer repository currently depends on Yasin-AI as a package dependency.** AI consumers implement local provider/adapters.
3. **AI duplication is real and verified:**
   - **YasinRelay:** `PassthroughProcessor` / `AIProcessor` calling OpenAI-compatible HTTP directly (`requests` to `/chat/completions`).
   - **YasinPress-Rewrite-:** Full local AI stack (`yasinpress/ai/*`: base, factory, openai_compatible, resilient, fallback, mock).
   - **Yasinfeed:** Local `AIRouter` + failover + prompts (minimal stub).
4. **Yasin-Agent** owns planning/workflow/tools/session; integrates **Yasin-Core SDK** (adapter), not Yasin-AI. README still describes the package as part of Yasin-AI historically — identity drift.
5. **YasinHub** is a lightweight status CLI (status store + process checker + registry), not a full control plane.
6. **Yasin-cli** default branch is `initial-setup` (not `main`); Node.js control surface; no verified Yasin-AI coupling.
7. **Ownership overlap:** Relay, Feed, and Press each implement collect → process/AI → publish style pipelines (documented in PHASE8_SOURCE_VERIFICATION).
8. **PROJECTS.md is stale on Yasin-AI version** (lists README v1.1.0; code is 1.1.4).
9. **Follow-up integration issues already exist** on consumer repos (Relay #43, Feed #52, and parallel ecosystem issues created with #7/#8). Phase 0 reuses them rather than duplicating.

---

## 3. Ecosystem Integration Matrix

| Repository | Version (verified) | Status | Architectural role | Ownership (ADR intent) | Dependencies (code evidence) | Public contracts | AI dependency | Yasin-AI integration | Test status | CI status | Production readiness | Known blockers | Remaining migration work |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **YASIN-DOCS** | n/a (docs hub) | Active | Ecosystem architecture & ADR SoT | Docs governance | None (docs only) | ADRs, matrices | N/A | Documents AI platform | Manual | N/A | Docs baseline | Stale version notes | Keep matrix current |
| **Yasin-core** | **3.3.0** | Release-freeze validation | Generic runtime/SDK foundation | Core | requests, dotenv, PyYAML; optional psutil | SDK, runtime, providers interfaces, agents primitives | Low-level provider interfaces only | Does not consume Yasin-AI | pytest present | Not fully verified this pass | Freeze for 3.3.0 | Doc/identity alignment | Keep foundation boundary; no AI platform ownership |
| **Yasin-AI** | **1.1.4** | Stable foundation / controlled integration | Canonical shared AI platform | AI platform | cryptography; optional pytest/ruff | `yasinai.contracts` v1, services, providers, integration clients | Is the AI platform | N/A (provider) | Extensive pytest suite in tree | CI workflows present | Controlled integration ready; not distributed HA | Plugin sandbox / HA planned only | Consumers must adopt public contracts |
| **Yasin-agent** | **1.0.0** | Stable package | Agent planning, workflow, tools, sessions | Agent execution | click; optional Yasin-Core SDK (adapter) | agent_platform public exports | Uses Core memory/tools; **no Yasin-AI import found** | **Not integrated** (deferred #19) | tests/ present | .github present | Application-stable; ecosystem AI path open | — | Optional adapter when needed |
| **YasinHub** | unversioned (README) | Lightweight | Status/health aggregation CLI | Status/observability | pytest for tests | status_store write API, CLI `status` | None verified | **Not required** | tests present | Unknown | Ops helper, not full control plane | — | Optional AI process health later |
| **Yasin-cli** | unversioned | Early | Unified user-facing command surface (target) | CLI control surface | Node.js, Jest | config/doctor/status/service/plugin | None verified | **Deferred** | npm test | Unknown | Not production-classified | Default branch still `initial-setup` (main exists; #34) | Later ecosystem commands |
| **YasinRelay** | **2.0.0** | Stable; AI + fetcher + secrets closed | Telegram→process→Eitaa relay pipeline | Domain/content relay | Yasin-AI adapter + legacy passthrough | pipeline stages, integration_registry, event bus | **Yasin-AI public contracts (default)** | **Integrated** (#43) | pytest; adapter + fetcher green | Unknown | Near-prod | Residual product roadmap only | Legacy path retained as fallback |
| **Yasinfeed** | unversioned | Active development | Feed collection, rewrite, publish | Feed ingestion/content pipeline | `yasinai_provider` + local providers | engine lifecycle, API, publisher | **Yasin-AI provider registered** | **Integrated** (#52) | unittest | Unknown | Not fully production | Product roadmap (#37,#42,…) | Prefer platform over new local stacks |
| **YasinPress-Rewrite-** | **1.0.0** | Runnable baseline | News RSS→AI enrich→queue→PWA/RSS/Eitaa | News processing & publishing | optional yasinai backend + CF default | CLI, publishing destinations | Optional `AI_BACKEND=yasinai` | **Optional path** | 114 tests claimed | Unknown | Strong local readiness | Python 3.13 floor | CF remains domain default |

---

## 4. Current-State Architecture Map (post-migration)

```text
                    [Users / Operators]
                            |
              +-------------+-------------+
              |                           |
         Yasin-cli (Node)            YasinHub (status CLI)
         (main branch exists)        status_store / pgrep
              |                           |
              +-------------+-------------+
                            |
        +-------------------+-------------------+
        |                   |                   |
   Yasin-agent         Yasin-core            Yasin-AI v1.1.4
   planner/executor    runtime/SDK           contracts / services
   tools/sessions      agents primitives     (public only)
        |              storage/obs                 ^
        +------ SDK adapter ------+                |
                                      adapters ----+
        +-------------------+----------------------+-------+
        |                   |                      |       |
   YasinRelay          Yasinfeed            YasinPress-Rewrite-
   TG collect          feed fetch           RSS fetch
   yasinai_adapter     yasinai_provider     optional yasinai
   (+ passthrough)     (+ legacy providers) (+ CF default)
   Eitaa publish       Eitaa/RSS/PWA        PWA/RSS/Eitaa
```

**AI edges:** consumers → public `yasinai.contracts` / `yasinai.services` only. No private module imports.

---

## 5–6. (Historical baseline — see original Phase 0 text and certification doc for pre-migration maps)

---

## 7. Integration Gap List — **RESOLUTION STATUS (2026-08-16)**

### P0 Critical — **CLOSED**

| ID | Gap | Resolution |
|---|---|---|
| P0-1 | Consumers do not use Yasin-AI public contracts | Relay #43, Feed #52, Press optional path — **DONE** |
| P0-2 | Duplicate OpenAI-compatible stacks | Canonical path via adapters; legacy retained as fallback — **DONE** |
| P0-3 | PROJECTS.md understates Yasin-AI version | Updated to **v1.1.4** + post-migration status — **DONE** |

### P1 High — **CLOSED / TRACKED**

| ID | Gap | Resolution |
|---|---|---|
| P1-1 | Relay Go fetcher / test failures | #35 closed; stub + path fixes; suite green — **DONE** |
| P1-2 | Relay historical secrets | #34 closed; rewrite + promote-to-main; `.env` absent from history — **DONE** |
| P1-3 | Overlapping content pipelines | Documented as acceptable independent products (`PIPELINE_OWNERSHIP.md`) — **DONE** |
| P1-4 | Hub over-documented | README already status-only; certification aligned — **DONE** |
| P1-5 | Agent README identity drift | README rewritten (independent agent platform + ADR-001) — **DONE** |
| P1-6 | Yasin-cli non-main default | `main` branch created; default flip = Yasin-cli **#34** (maintainer Settings) — **TRACKED** |

### P2 / P3

Remain product/roadmap items (Feed #37/#42, Press Python floor, Agent optional AI #19, CLI ecosystem commands). Out of Phase-0 P0/P1 scope.

---

## 8–13. (Original sequence, issues, contradictions, exit criteria preserved)

Phase 0 exit criteria were met at baseline time. Post-Phase-0 execution completed the P0/P1 gap list above.

---

## 14. Post-Phase-0 execution close-out

| Item | Evidence |
|------|----------|
| Yasin-AI contracts unchanged | v1.1.4 public surface |
| Relay AI adapter | `yasinrelay/yasinai_adapter.py` + `tests/test_yasinai_adapter.py` (private-import guard) |
| Feed AI provider | `yasinfeed/rewrite/providers/yasinai_provider.py` |
| Press optional backend | per certification |
| Secrets history | YasinRelay main clean of `.env` path |
| Fetcher | #35 closed |
| Docs | `PROJECTS.md`, certification, this file, `PIPELINE_OWNERSHIP.md` |
| Agent identity | README on main |
| CLI branch | `main` exists; default still `initial-setup` until Settings change |

**Certified companion:** `docs/audits/ECOSYSTEM_POST_PHASE0_CERTIFICATION.md` (YASIN-DOCS #8).

**No further P0/P1 work remains in the Phase-0 gap list.**
