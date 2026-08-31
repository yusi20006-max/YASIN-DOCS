# Yasin-MCP — Termux Integration and Hardening Record

**Date:** 2026-08-31  
**Repository:** `yusi20006-max/Yasin-MCP`  
**Documentation scope:** Termux installation/runtime validation, MCP governance fixes, and the final GitHub/CI state reached during the integration work.

---

## 1. Executive summary

Yasin-MCP was taken through a full Termux troubleshooting and GitHub hardening cycle. The work started with broken virtual environments and dependency installation failures, then moved through missing test dependencies and a governed MCP callable-signature regression. The resulting repository state is green on GitHub and the latest `main` commit is the merged PR #113 fix.

The key outcome is that native Termux/Android no longer attempts to install Ruff, while supported CI platforms retain the Ruff quality gate. The governed MCP wrapper also preserves the concrete callable signature required for MCP schema generation without triggering the Bandit quality gate.

---

## 2. Repository and final GitHub state

`Yasin-MCP` is the MCP server and AI access layer for the Yasin ecosystem.

Latest verified `main` commit:

- `5750a423250ced602b76e97050fabbc418730854`
- Commit: `fix: satisfy Bandit for governed signature assignment (#113)`
- PR #113: merged
- GitHub CI run #411: **success**
- Workflow run: `33330680472`

The CI run for this exact commit completed successfully on 2026-08-30. citeturn704file0

The latest main commit is signed/verified by GitHub and contains the final Bandit/mypy-compatible signature assignment. citeturn703file0

There are currently no open PRs in `Yasin-MCP`.

---

## 3. Termux virtual-environment failure and recovery

The first clean clone/retest exposed a broken `.venv` state:

```text
.venv/bin/python: No such file or directory
.venv/bin/activate: No such file or directory
```

The environment was therefore not reused. The repository was removed and cloned again, `VIRTUAL_ENV` was cleared, the shell hash was reset, and a completely new virtual environment was created.

The successful recovery sequence was:

```bash
cd ~
rm -rf Yasin-MCP
git clone https://github.com/yusi20006-max/Yasin-MCP.git
cd Yasin-MCP
unset VIRTUAL_ENV
hash -r
python -m venv .venv
source .venv/bin/activate
python --version
python -m pip install -U pip setuptools wheel
python -m pip install -e .
```

The verified Termux interpreter was:

```text
Python 3.14.6
```

Runtime installation completed successfully after rebuilding the environment.

---

## 4. Ruff / native Termux policy

Ruff is a development-time linter/formatter. It is not required for Yasin-MCP runtime execution.

Native Termux/Android repeatedly failed while attempting to build/install Ruff. This was treated as an environment compatibility problem rather than a runtime application dependency.

The repository was changed so that the `dev` dependency for Ruff is conditional:

```toml
"ruff>=0.4.0; platform_system != 'Android'",
```

Therefore:

- native Termux/Android: **do not install Ruff**;
- supported CI platforms: Ruff remains part of the development environment and quality gate.

This policy was implemented and merged in **PR #112**, titled `fix: skip Ruff installation on native Termux`. The PR explicitly verifies that native Termux must not install Ruff while Ubuntu CI continues to run Ruff. citeturn701file0turn703file0

The current `pyproject.toml` confirms the Android marker remains in the repository. citeturn701file0

### Operational rule

For Yasin projects running natively in Termux, do not make Ruff a prerequisite for installation or runtime testing. Keep lint/format quality gates on supported CI platforms instead.

---

## 5. Runtime vs development dependencies

A runtime-only installation with:

```bash
python -m pip install -e .
```

does not install the complete `dev` dependency set.

This caused an expected failure when the test suite was invoked without pytest in the virtual environment:

```text
No module named pytest
```

The repository's `dev` extras contain test tooling including pytest and pytest-cov, plus mypy, Bandit, types-PyYAML, and httpx. Ruff is the only development dependency explicitly excluded on Android. citeturn701file0

Therefore the correct distinction is:

```text
runtime install
    → python -m pip install -e .
    → MCP runtime dependencies only

full development/test environment
    → python -m pip install -e '.[dev]'
    → pytest + coverage + static/security tooling
    → Ruff omitted automatically on Android
```

If a test imports `httpx`, the development/test environment must contain the `httpx` dev dependency; this is not a reason to add it to the runtime dependency set unless runtime code actually imports it.

---

## 6. MCP governed-tool signature regression

A regression was found in:

```text
tests/test_governance.py
```

The affected test verifies that `GovernanceGate.wrap_tool()` preserves the concrete callable signature needed for MCP schema generation:

```text
owner: str
repository: str
limit: int = 20
```

The failure appeared as:

```text
assert 'str' is str
```

The underlying issue was postponed/quoted annotations caused by the module's future-annotations behavior. The MCP schema path must receive concrete type information rather than string annotations.

PR #111 introduced explicit preservation of the wrapped callable signature using `__signature__`. The regression test verifies the expected parameter names, annotations, default value, and actual invocation behavior. citeturn706file0turn701file0

---

## 7. Bandit quality-gate regression after the signature fix

The first signature-preservation implementation used:

```python
setattr(sync_wrapper, "__signature__", signature)
```

Bandit B010 rejected this pattern. The CI quality gate therefore failed even though the runtime intent was valid.

PR #113 changed the assignment to a direct attribute assignment through a typing cast:

```python
cast(Any, sync_wrapper).__signature__ = signature
```

This preserves the required signature while satisfying the existing security/static-analysis gate. The final commit also includes the mypy-compatible typing adjustment. citeturn703file0

PR #113 is merged and its exact GitHub Actions CI run is green. citeturn704file0

---

## 8. Termux compatibility hardening history

PR #110 aligned the Termux compatibility regression tests with the verified native Termux runtime instead of preserving obsolete unsupported-environment assumptions. It removed obsolete native-Termux skips for cryptography and MCP import tests while retaining the relevant Termux/cryptography/PyLong_Type boundary checks. citeturn701file0

PR #112 then made the dependency installation behavior explicit: Ruff is skipped only on native Android/Termux while remaining available to supported CI environments. citeturn701file0

PR #113 resolved the final Bandit/mypy quality-gate issue created by the governed signature preservation work. citeturn703file0

The three changes form one coherent hardening sequence:

```text
#110  Termux compatibility contract
          ↓
#112  no-Ruff native Termux installation
          ↓
#113  governed MCP signature + CI quality gate
          ↓
       GREEN main
```

---

## 9. Verified GitHub CI evidence

The final `main` commit is:

```text
5750a423250ced602b76e97050fabbc418730854
```

The exact workflow associated with that SHA is:

```text
Workflow: CI
Run: #411
Run ID: 33330680472
Status: completed
Conclusion: success
Workflow file: .github/workflows/ci.yml
```

This is the authoritative GitHub CI evidence for the final state. citeturn704file0

---

## 10. Final Termux installation guidance

For a clean native Termux validation, use a fresh environment and install runtime dependencies first:

```bash
cd ~
rm -rf Yasin-MCP
git clone https://github.com/yusi20006-max/Yasin-MCP.git
cd Yasin-MCP
unset VIRTUAL_ENV
hash -r
python -m venv .venv
source .venv/bin/activate
python --version
python -m pip install -U pip setuptools wheel
python -m pip install -e .
```

For running the test suite, install the development extras as well:

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
```

On native Android/Termux, the Ruff dependency is automatically excluded by the platform marker. Do not manually install Ruff as part of the standard Yasin Termux setup.

---

## 11. MCP live-runtime validation target

Unit/CI status is green, but the next integration-level validation remains the actual MCP protocol path:

```text
initialize
    ↓
list_tools
    ↓
inspect tool schemas
    ↓
call_tool
    ↓
verify governed GitHub operation
```

The purpose is to confirm that the concrete callable signatures preserved by the governance layer are correctly exposed through the MCP server to an actual MCP client.

This is distinct from pytest and should be treated as live protocol/integration evidence.

---

## 12. Relationship to the wider Yasin ecosystem

Yasin-Agent was already active during this work and was not recreated or replaced.

YasinHub is the control/orchestration boundary. Its recent work is already merged and locally verified separately.

Yasin-MCP is the AI/Agent-facing MCP access and integration layer. Its role is to expose governed, policy-controlled capabilities to MCP clients without bypassing YasinHub or the defined governance boundary.

The intended direction remains:

```text
MCP Client
    ↓
Yasin-MCP
    ↓
Governance / Policy / Audit
    ↓
Approved integration surfaces
    ↓
YasinHub / GitHub / ecosystem APIs
```

No new direct Agent runtime is introduced by this work.

---

## 13. Final status

**Yasin-MCP Termux/CI hardening: GREEN**

Completed and merged:

- [x] broken Termux virtual environment recovery procedure established;
- [x] Python 3.14.6 Termux environment verified;
- [x] runtime dependency installation verified;
- [x] native Android/Termux Ruff installation removed via environment marker;
- [x] Termux compatibility regression contract reconciled;
- [x] governed MCP callable signature preservation implemented;
- [x] regression test for `owner`, `repository`, and `limit` retained;
- [x] Bandit B010 quality-gate issue fixed;
- [x] mypy compatibility fixed;
- [x] PR #110 merged;
- [x] PR #111 merged;
- [x] PR #112 merged;
- [x] PR #113 merged;
- [x] exact final GitHub CI run green;
- [x] no open Yasin-MCP PR remains.

### Next integration step

Proceed with the live MCP client validation (`initialize → list_tools → call_tool`) and then continue the Yasin-MCP ↔ YasinHub integration path.
