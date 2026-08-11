# Phase 8 — YasinCLI Code Audit Pass 2

- Date: 2026-08-11
- Repository: `yusi20006-max/Yasin-cli`
- Audited branch: `initial-setup`
- Status: Evidence recorded (Level 1 — source verified, confirmed by direct execution)

## 1. Purpose

Pass 1 (`PHASE8_CODE_AUDIT_YASIN_CLI_PASS1.md`) recorded the architecture-level
role of YasinCLI. This pass records an implementation-level defect found by
directly executing the CLI, which Pass 1 did not cover.

## 2. Finding: Total CLI Crash (now fixed)

**Evidence level: Source verified.** Confirmed by running `node src/index.js`
(no arguments) on `initial-setup` before the fix below: every invocation
raised `SyntaxError: missing ) after argument list` and exited before
printing anything, including `--help`.

**Root cause:** `src/dev/ProjectScaffolder.js` contained a template literal
with an over-escaped backtick (two backslashes instead of one), which
terminated the string early. Because `src/index.js` eagerly `require()`s
every command module — including `src/commands/create.js`, which requires
`ProjectScaffolder.js` — this one syntax error made the entire CLI
unusable, not just the `create` command.

**Secondary finding surfaced while fixing the above:** once the file could
be parsed, `tests/scaffolder.test.js` (previously unable to run at all)
revealed that `createAdapter()` unconditionally appended an `Adapter`
suffix to the generated class name, producing `DemoAdapterAdapter.js` for
an input name that already ended in `adapter` (e.g. `demo-adapter`), instead
of the expected `DemoAdapter.js`.

**Also found:** `tests/lifecycle.test.js` was written against a stale
contract — it constructed `LifecycleCommand` with a raw adapter array,
while the actual class and the production wiring in `src/index.js` both
expect an `EcosystemOrchestrator` instance. The test could not have been
passing against the real production contract.

## 3. Fix Status

**Fixed.** PR `yusi20006-max/Yasin-cli#29`, merged into `initial-setup`.

Verification performed (per `AI_TESTING_VALIDATION_PROTOCOL.md`):
- Direct execution: `help`, `status`, `doctor`, `create plugin|service|adapter`
  all run without crashing (previously: 100% crash rate on every command).
- `npx jest`: 17/17 suites, 83/83 tests passing (previously: 3 suites failed
  to load, plus 2 additional test failures once loadable).
- `npx eslint src tests`: 0 errors (previously: 1 parsing error, same file).
- `npm run smoke`: passes.

Also fixed in the same PR: `AUDIT_REPORT.md` item L-01 (hardcoded `'1.0.0'`
version fallback duplicated in `CommandRegistry.js` and `status.js`),
consolidated into `src/core/version.js`.

Also verified (not changed, already correct in current code):
`AUDIT_REPORT.md` items M-01 (PID recycling — `ServiceManager.isProcessOwned`
already checks process identity) and M-02 (Windows shell injection —
`spawn()` already hardcodes `shell: false`).

## 4. CI Discrepancy — RESOLVED (update: 2026-08-11)

**Original observation (recorded above, now superseded):** the
`phase-4-5-1-ci.yml` workflow failed on all 9 OS/Node combinations both
before and after the Pass 2 fix, and was recorded as Level 5 — Unknown
pending full log access.

**Root cause found (Source verified, PR `Yasin-cli#30`, merged):** the
workflow's "Lockfile contract" step ran
`npm test -- --runInBand tests/lockfile-contract.test.js`, but that file
never existed in the repository. Reproduced locally: running that exact
command exits with code 1 ("No tests found") on any OS/Node version,
which matches the CI history exactly. This was a missing file, not a
runner/environment flake.

**Fix:** added `tests/lockfile-contract.test.js` (4 checks: lockfile
version, name match, dependency presence, and a real `npm ci --dry-run`
against the committed lockfile). This alone brought 6 of 9 combinations
(all ubuntu/macos) to green.

**Secondary, OS-specific bug found while fixing the above:** the
remaining 3 failures (all `windows-latest`, every Node version) were a
second, independent bug introduced by the fix itself:
`execFileSync('npm', ...)` without `shell: true` throws `ENOENT` on
Windows, because `npm` resolves to `npm.cmd` there, which
`execFileSync` cannot invoke directly without shell involvement. Added
`shell: process.platform === 'win32'` to the same call.

**Final state, confirmed via GitHub check-runs (not assumed):** all 9
`phase-4-5-1-ci.yml` matrix combinations pass, plus `test` and
`release-check`.

## 5. Remaining Known Gaps (unchanged from Pass 1 / AUDIT_REPORT.md)

- L-02 (custom argument parser edge case for negative numbers) — open,
  documentation-only fix, not yet done.
- Yasin-AI adapter integration — still absent from `createEcosystemAdapters()`
  (Pass 1 finding, unchanged). This is an L3 cross-project contract change
  per `AI_CHANGE_IMPACT_PROTOCOL.md` and requires inspecting Yasin-AI's
  public API (`docs/api/YASIN_AI_PUBLIC_API_V1.md`) before implementation.
- YasinFeed / YasinPress adapter integration — same status as Pass 1.

## 6. Next Step

Proceed to the Yasin-AI adapter gap identified in Pass 1, following the
L3 change procedure in `AI_CHANGE_IMPACT_PROTOCOL.md` (inspect
`docs/api/YASIN_AI_PUBLIC_API_V1.md` before implementation).
