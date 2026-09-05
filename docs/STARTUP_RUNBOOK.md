# Yasin Ecosystem Startup Runbook

**Status:** Canonical operational runbook
**Acceptance anchor:** YasinHub Issue #174
**Milestone:** #1 — Yasin Ecosystem — Final Acceptance & Operational Readiness
**Platform:** Android 11 / Termux / ARM64

## 1. Authority and boundaries

YasinHub is the sole Control Plane and lifecycle/PID authority. The PWA observes and requests lifecycle operations through YasinHub; it must not maintain an independent process state. Yasin-Agent consumes the Hub contract and must not become a second lifecycle authority. YasinRelay is the canonical process boundary for the publishing runtime. Yasin-AI is the canonical AI capability/provider boundary.

Canonical flow:

```text
PWA → YasinHub → Yasin-Agent → YasinRelay
                  ↓
               Yasin-AI
```

## 2. Startup order

1. Enter the intended Termux project environment.
2. Verify repository state and Python/runtime prerequisites.
3. Verify the operator configuration without printing secrets.
4. Start/control services through YasinHub only.
5. Verify real process identity and PID state from Hub responses.
6. Open the PWA/dashboard and treat Hub backend state as authoritative.
7. Run real publish acceptance only when valid operator credentials/configuration are provisioned.

Do not use a second launcher or manually-maintained PID state as a replacement for Hub lifecycle authority.

## 3. Canonical Relay launcher

YasinRelay's canonical Termux launcher is:

```text
.venv/bin/yasinrelay-termux run --schedule --non-interactive
```

The launcher must be executed with `shell=False` semantics and its process identity must be verified by the Control Plane before a start operation is reported successful.

## 4. Required operator configuration

The following values may be required for a real publish run:

- `SOURCE_CHANNELS`
- `EITAA_TOKEN`
- `EITAA_CHANNEL`
- `AI_API_KEY`
- `AI_PROVIDER=yasinai`
- `OPENAI_API_KEY` (only where the configured provider requires it)

Credentials are operator-provided runtime configuration. Never invent, echo, commit, or include secret values in reports, logs, issues, or documentation.

Recommended local permission:

```text
.env = 0600
```

The `.env` file must remain excluded from Git.

## 5. Truthful startup behavior

A successful start means more than a process object being created. YasinHub must verify that the expected process remains alive and corresponds to the intended service identity.

For an invalid/empty publish configuration, truthful behavior is failure, not a fake RUNNING state. Expected signals include:

- `success=false`
- no authoritative PID retained after failed startup
- `process_running=false`
- health state `FAILED` or equivalent truthful failure state

A short-lived Relay process must not leave a stale or zombie PID represented as RUNNING.

## 6. Lifecycle acceptance

For a real service lifecycle, verify:

### Start
- Hub returns success only after process verification.
- Returned PID is a real OS PID.
- PID belongs to the expected process identity.

### Stop
- Hub requests termination.
- The process is confirmed dead.
- The old PID is not reported as running.

### Restart
- The previous process is dead.
- A new process is started and verified.
- The new PID is different when the OS allocates a different process identity.

### Recovery
- Failed startup removes stale PID state.
- Process disappearance is reflected truthfully in Hub state.
- PID checks use OS-level process verification rather than dashboard-only state.

## 7. PWA operation

The PWA is an operational interface to YasinHub. Start/stop/restart controls must rely on the authoritative Hub response and must not optimistically display success when the backend reports failure.

For final visual acceptance, use a real browser on the target mobile viewport. Static source inspection or an HTTP 200 response is not sufficient to claim visual acceptance.

## 8. Health and diagnostics

Use Hub health/readiness and service-status endpoints to verify:

- Hub is reachable.
- Service state reflects the real process.
- PID information is consistent with process liveness.
- Failure states are explicit and truthful.
- No secret material appears in diagnostics.

## 9. Real publish acceptance

Real publishing is an operator-gated test. Before running it, provision valid runtime configuration locally and keep all credentials out of Git.

Acceptance requires evidence of the actual chain:

```text
Hub command
  → real Relay process
  → configured source/feed processing
  → AI capability path
  → publish operation
  → truthful resulting status
```

If required configuration is absent, record the run as **OPERATOR-BLOCKED**, not PASS.

## 10. Security rules

- No `shell=True` for lifecycle commands.
- Parse command arguments safely.
- Verify process identity before declaring success.
- Use OS-level liveness checks where required.
- Never print tokens/API keys.
- Never commit `.env` or credentials.
- Fail closed on missing/invalid authorization/configuration.
- Keep YasinHub as the single lifecycle/PID authority.

## 11. Current verified acceptance baseline

The final Issue #174 software/device regression established the following baseline:

- YasinHub: 478 tests passed.
- Yasin-Agent: 240 tests passed.
- YasinRelay: 108 tests passed.
- Yasin-AI: 415 tests passed on the Termux environment using the compatible installed crypto stack.
- Real PID lifecycle machinery was verified, including start/stop/restart and short-lived-process/zombie prevention.
- PWA backend/API control-path checks passed.
- Security checks passed.

These results do not convert the remaining external acceptance blockers into a PASS.

## 12. Remaining acceptance gates

At the latest Issue #174 checkpoint, two external gates remained:

1. **Real publish:** requires valid operator-provided `SOURCE_CHANNELS`, Eitaa configuration, and AI credentials/configuration.
2. **PWA visual acceptance:** requires execution in a real browser/mobile viewport and visual verification of the acceptance checklist.

Once those gates are provisioned and executed, update the Issue #174 final report and rerun the final regression/acceptance checkpoint. Do not restart completed phases.

## 13. Evidence rule

Every operational claim must be backed by command output, test output, API response, process/PID evidence, or browser evidence. A static source inspection can establish implementation intent but cannot substitute for runtime or visual acceptance where runtime/visual proof is required.
