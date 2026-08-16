# Ecosystem Re-baseline — Phase 0

**Issue:** YASIN-DOCS #7  
**Date:** 2026-08-16  
**Status:** Complete (documentation baseline)  
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
| 6 | `yusi20006-max/Yasin-cli` | `initial-setup` | README (Node.js CLI) |
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
| **Yasin-agent** | **1.0.0** | Stable package | Agent planning, workflow, tools, sessions | Agent execution | click; optional Yasin-Core SDK (adapter) | agent_platform public exports | Uses Core memory/tools; **no Yasin-AI import found** | **Not integrated** | tests/ present | .github present | Application-stable; ecosystem AI path open | README identity drift vs Core adapter | Adapter to Yasin-AI generation/memory contracts when needed |
| **YasinHub** | unversioned (README) | Lightweight | Status/health aggregation CLI | Status/observability (target: lifecycle) | pytest for tests | status_store write API, CLI `status` | None verified | **Not integrated** | tests present | Unknown | Ops helper, not full control plane | Over-documented as control plane | Optional status of Yasin-AI service only |
| **Yasin-cli** | unversioned | Early (`initial-setup`) | Unified user-facing command surface (target) | CLI control surface | Node.js, Jest | config/doctor/status/service/plugin | None verified | **Not integrated** | npm test | Unknown | Not production-classified | Non-main default branch | Later adapter to ecosystem services |
| **YasinRelay** | **2.0.0** | Stable feature set; open hardening issues | Telegram→process→Eitaa relay pipeline | Domain/content relay | requests (AI HTTP), SQLite, Go fetcher | pipeline stages, integration_registry, event bus | **Local OpenAI-compatible HTTP** | **Not integrated** | pytest; known Go fetcher failures (#35) | Unknown | Near-prod with blockers | Secrets history #34; fetcher #35; AI migration #43 | Migrate AI to Yasin-AI public contracts |
| **Yasinfeed** | unversioned (v1.0 release issue open) | Active development | Feed collection, rewrite, publish | Feed ingestion/content pipeline | local modules | engine lifecycle, API, publisher stubs | **Local AIRouter stub** | **Not integrated** | unittest; port conflict issue #37 | Unknown | Not fully production | AI multi-provider #42; integration #45/#52 | Integrate Yasin-AI via adapter |
| **YasinPress-Rewrite-** | **1.0.0** | Runnable baseline | News RSS→AI enrich→queue→PWA/RSS/Eitaa | News processing & publishing | httpx, feedparser, PyYAML; **Python ≥3.13** | CLI, publishing destinations, AI provider interface | **Local AI provider stack** | **Not integrated** | 114 tests claimed in registry | Unknown | Strong local readiness; live creds pending | Python 3.13 floor vs ecosystem 3.9+ | Migrate AI layer to Yasin-AI contracts |

---

## 4. Current-State Architecture Map

```text
                    [Users / Operators]
                            |
              +-------------+-------------+
              |                           |
         Yasin-cli (Node)            YasinHub (status CLI)
         (initial-setup)             status_store / pgrep
              |                           |
              +-------------+-------------+
                            |
        +-------------------+-------------------+
        |                   |                   |
   Yasin-agent         Yasin-core            Yasin-AI
   planner/executor    runtime/SDK           providers/services
   tools/sessions      agents primitives     contracts v1
        |              storage/obs           knowledge/memory (private)
        +------ SDK adapter ------+                 ^
                                      (intended)   |
                                      (not wired)  |
        +-------------------+----------------------+-------+
        |                   |                      |       |
   YasinRelay          Yasinfeed            YasinPress-Rewrite-
   TG collect          feed fetch           RSS fetch
   local AI HTTP       local AIRouter       local AI providers
   Eitaa publish       Eitaa/RSS/PWA        PWA/RSS/Eitaa
   SQLite              SQLite               SQLite + queue
```

**Actual AI edges today:** dashed/local only. No package dependency edge from Relay/Feed/Press/Agent → Yasin-AI.

---

## 5. Dependency / Ownership Map

### Intended ownership (ADR-001 + related)

| Project | Owns | Must not own |
|---|---|---|
| Yasin-Core | Generic runtime, SDK, low-level provider interfaces, execution primitives | Ecosystem AI platform, domain pipelines |
| Yasin-AI | Shared AI capabilities, provider routing, RAG/memory platform contracts | Agent execution semantics, business/content logic |
| Yasin-Agent | Planning, workflow, tools, sessions | AI provider platform |
| YasinHub | Status / lifecycle observability (current: status only) | Domain processing |
| YasinCLI | User-facing command surface | Domain engines |
| YasinRelay | Relay pipeline domain | Shared AI infrastructure |
| YasinFeed | Feed ingestion & content pipeline | Shared AI infrastructure |
| YasinPress | News processing, queue, publishing | Shared AI infrastructure |
| YASIN-DOCS | Cross-repo architecture & ADRs | Implementation |

### Observed depends-on (implementation)

```text
Yasin-agent  --(PUBLIC intended SDK)-->  Yasin-core   [adapter present; Core may be mocked in tests]
YasinRelay   --(PRIVATE local)-------->  OpenAI-compatible HTTP API
YasinRelay   --(soft)----------------->  YasinHub status_store (hub_integration.py)
Yasinfeed    --(PRIVATE local)-------->  AIRouter stubs
YasinPress   --(PRIVATE local)-------->  OpenAI-compatible client abstraction
Yasin-AI     --(none to apps)--------->  does not depend on Agent/Relay/Feed/Press private code
Yasin-AI     --(reference only)------->  yasinai.integration.* clients (not required by apps)
```

**Public contract path (target):**  
`Consumer → yasinai.contracts / yasinai.services / yasinai.providers → Runtime`

**Private (forbidden for consumers):**  
`knowledge_platform`, `developer_platform`, `security_platform`, SQLite internals, provider client internals.

---

## 6. AI Integration Matrix

| Repository | Uses AI? | Where implemented | Provider abstraction | Duplicated AI infra? | Direct provider SDK/HTTP? | Consumes Yasin-AI? | Public contract used | Migration required | Private Yasin-AI imports? | Yasin-AI depends on app? | Adapter needed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Yasin-core | Interfaces only | providers/ package | Low-level interfaces | N/A | No verified SDK calls in this pass | No | N/A | Keep boundary | No | No | None |
| Yasin-AI | Yes (platform) | providers, services, knowledge | Full | Canonical | OpenAI/Anthropic/Local adapters | Self | contracts v1 | Maintain | N/A | No | N/A |
| Yasin-agent | Indirect (via tools/Core) | No local LLM client found | None local | Memory/context local to agent | No | **No** | — | Optional generation/memory via Yasin-AI | No | No | Optional Agent↔AI client |
| YasinHub | No | — | — | No | No | No | — | Optional health only | No | No | Optional |
| Yasin-cli | No | — | — | No | No | No | — | Later diagnostics | No | No | Later |
| YasinRelay | **Yes** | `ai_processor.py` | AIProcessor ABC | **Yes** | **Yes** (requests → chat/completions) | **No** | — | **Yes — primary** | No | No | ContentProcessor → GenerationService |
| Yasinfeed | **Yes (stub)** | `yasinfeed/ai/*` | AIRouter | **Yes (minimal)** | Not full SDK; stub failover | **No** | — | **Yes** | No | No | rewrite → Generation/RAG |
| YasinPress | **Yes** | `yasinpress/ai/*` | AIProvider + factory | **Yes** | OpenAI-compatible client | **No** | — | **Yes — primary** | No | No | enrich → GenerationService |

---

## 7. Integration Gap List

### P0 Critical

| ID | Gap | Evidence | Owner |
|---|---|---|---|
| P0-1 | Consumers do not use Yasin-AI public contracts for AI | No package deps; local HTTP/stubs | Relay, Feed, Press |
| P0-2 | Duplicate OpenAI-compatible generation stacks | Relay ai_processor; Press openai_compatible | Relay, Press |
| P0-3 | PROJECTS.md / registry understates Yasin-AI version (1.1.0 vs **1.1.4**) | PROJECTS.md vs pyproject | YASIN-DOCS |

### P1 High

| ID | Gap | Evidence | Owner |
|---|---|---|---|
| P1-1 | Relay Go fetcher / test failures | Issue #35 (83 pass / 8 fail reported) | YasinRelay |
| P1-2 | Relay historical secrets cleanup | Issue #34 | YasinRelay |
| P1-3 | Overlapping content pipelines (Feed vs Relay vs Press) | PHASE8 + READMEs | Architecture (DOCS) + domain owners |
| P1-4 | Hub documented broader than implementation | Status-only CLI vs “control plane” | YASIN-DOCS / Hub |
| P1-5 | Agent README identity still “YasinAI component” | README Persian header | Yasin-agent |
| P1-6 | Yasin-cli on non-main default branch | `initial-setup` | Yasin-cli |

### P2 Medium

| ID | Gap | Evidence | Owner |
|---|---|---|---|
| P2-1 | Feed AI multi-provider incomplete | Issue #42; thin AIRouter | Yasinfeed |
| P2-2 | Feed engine port test flakiness | Issue #37 | Yasinfeed |
| P2-3 | Core contains agents/ + execution while Agent is higher platform | Tree + ADR-0003 PARTIAL | Core/Agent wording |
| P2-4 | Press requires Python ≥3.13 vs ecosystem ≥3.9 | pyproject | YasinPress |
| P2-5 | No cross-repo contract tests in consumers | Consumer trees | Each consumer |

### P3 Low

| ID | Gap | Evidence | Owner |
|---|---|---|---|
| P3-1 | Hub optional status reporting for AI service | Missing | Hub |
| P3-2 | CLI ecosystem service plugins | Not present | Yasin-cli |
| P3-3 | Version tags/releases not uniformly published | Metadata pass incomplete | All |

---

## 8. Integration Sequence (Dependency-Safe)

Do **not** migrate consumers before contracts are treated as frozen (they already are in Yasin-AI docs for v1).

```text
1. YASIN-DOCS     — baseline matrix, version truth, ADR current-state notes  [THIS PHASE]
2. Yasin-AI       — freeze/verify public contract tests remain green (already v1.1.4)
3. Yasin-core     — remain foundation; no AI platform expansion
4. Yasin-agent    — optional AI capability via public contracts only (after Core stability)
5. YasinHub       — status only; optional AI process health later
6. YasinRelay     — AI adapter migration (issue #43); after fetcher/secrets P1s as needed
7. Yasinfeed      — AI adapter (issue #52); parallelizable with Relay after contracts
8. YasinPress     — AI adapter; note Python version constraint
9. Yasin-cli      — last: aggregate commands after services expose stable status APIs
10. YASIN-DOCS #8 — E2E certification only after above integrations complete
```

**Rationale:** AI platform is already the stable provider. Highest duplication and production AI usage are Relay and Press; Feed is thinner. CLI and Hub are not AI blockers.

---

## 9. Follow-up Issues (Reuse, Do Not Duplicate)

| Task | Owning repo | Existing issue | Scope summary | Acceptance (from issue) |
|---|---|---|---|---|
| Ecosystem baseline | YASIN-DOCS | **#7** (this) | Matrix + maps + gaps | Verified baseline |
| E2E certification | YASIN-DOCS | **#8** | After integrations | Contract-verified ecosystem |
| Relay → Yasin-AI | YasinRelay | **#43** | Migrate AI to public contracts | No private imports; tests |
| Feed → Yasin-AI | Yasinfeed | **#52** | AI processing layer | Adapter; failure-safe |
| Relay fetcher | YasinRelay | **#35** | Go binary / tests 91/91 | Clean checkout |
| Relay secrets | YasinRelay | **#34** | History secret purge | Scan clean |
| Feed multi-provider | Yasinfeed | **#42** | Provider registry (prefer Yasin-AI over new local) | Prefer platform contracts |
| Feed ecosystem adapters | Yasinfeed | **#45** | Core/Agent/Hub/Relay adapters | No duplication |

**New issues:** None required for AI migration paths already covered. Optional future issues (not created in Phase 0 code changes):

- YasinPress: explicit “Migrate AI to Yasin-AI contracts” if not already filed under that repo.
- Yasin-agent: “Optional Yasin-AI generation/memory adapter”.
- YASIN-DOCS: ADR wording updates for Hub current-state and pipeline overlap (documentation-only).

---

## 10. Ownership Contradictions vs ADR Intent

| Contradiction | ADR intent | Code reality |
|---|---|---|
| AI platform ownership | Yasin-AI sole shared AI | Relay/Feed/Press implement local AI |
| Hub management boundary | Primary control/lifecycle | Status CLI only |
| Agent separation | Agent owns execution semantics | Core still has agents/ and execution packages (layered, not exclusive) |
| Feed vs Relay publishing | Distinct pipelines | Both fetch/process/publish |
| Agent identity | Independent agent platform | README still frames package as Yasin-AI component |
| CLI branch | Production control surface candidate | Default branch `initial-setup` |

---

## 11. Documentation Changes in This Phase

- Added this file: `docs/audits/ECOSYSTEM_REBASELINE_PHASE0.md`
- Updated `PROJECTS.md` Yasin-AI version evidence to **v1.1.4**
- No application code migrated; no consumer repos modified

---

## 12. Unresolved Decisions

1. **Pipeline exclusivity:** Whether Feed, Relay, and Press remain parallel domain apps or converge under a single content ownership ADR (ADR-0010 still needs rewrite per Phase 8).
2. **Agent AI path:** Whether Agent must call Yasin-AI for LLM steps or only domain apps do.
3. **Python version matrix:** Press 3.13+ vs Core/AI 3.9+ — compatibility policy for shared contracts.
4. **Hub expansion:** Whether Hub grows beyond status or stays a thin reporter.

---

## 13. Exit Criteria Checklist (Phase 0)

- [x] Every listed repository audited at metadata/README/structure level
- [x] Current versions verified where package metadata exists (AI 1.1.4, Core 3.3.0, Agent 1.0.0, Relay 2.0.0, Press 1.0.0)
- [x] Ownership documented vs ADR-001
- [x] Dependencies documented (public vs private)
- [x] AI usage documented per repo
- [x] Yasin-AI integration status verified (**none wired**)
- [x] Duplicate AI implementations identified
- [x] Private cross-repo deps: none found into Yasin-AI private modules; local provider coupling only
- [x] Architecture drift documented
- [x] Remaining work has owners via existing issues
- [x] Execution order established
- [x] YASIN-DOCS updated with verified current state

**STOP after this phase. Do not auto-start consumer implementation.**
