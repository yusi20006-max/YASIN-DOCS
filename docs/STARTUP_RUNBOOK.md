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

### 3.1 Canonical operator configuration path

The canonical Relay CLI uses `configure_interactively()` for a normal interactive `run` when no explicit channel override is supplied. This path is implemented in `yasinrelay/cli.py` and `yasinrelay/config.py`.

The important distinction is:

- **Interactive configuration:** run the normal interactive Relay `run` path from a real TTY; it invokes `configure_interactively()` and persists the entered runtime settings to the local `.env`.
- **Service/control-plane execution:** use the stored `.env` with `run --schedule --non-interactive`; do not depend on interactive prompts when YasinHub launches the service.
- **Lifecycle authority:** even though the Relay launcher is canonical, lifecycle start/stop/restart for acceptance must be requested through YasinHub, not by manually launching Relay from a second terminal.

The interactive configuration currently prompts for these settings, in this order:

1. `EITAA_TOKEN` — required secret.
2. `EITAA_CHANNEL` — required destination channel.
3. `SOURCE_CHANNELS` — required comma-separated source channels.
4. `AI_PROVIDER` — defaults to `yasinai`.
5. `AI_API_KEY` — optional secret; falls back to `OPENAI_API_KEY` when unset.
6. `AI_MODEL` — defaults to `gpt-4o-mini`.
7. `AI_BASE_URL` — defaults to `https://api.openai.com/v1`.
8. `FETCH_INTERVAL_SECONDS` — defaults to `3600`.
9. `INTER_MESSAGE_DELAY_SECONDS` — defaults to `15`.
10. `DATABASE_PATH` — defaults to `relay.db`.
11. `LOG_LEVEL` — defaults to `INFO`.
12. `EVENT_BUS_ENABLED` — defaults to `true`.
13. `EVENT_LOGGING_ENABLED` — defaults to `true`.

Pressing Enter keeps the previous value when one is already present. The configuration writer sets the `.env` permission to `0600` where supported.

**Secret-handling rule:** this runbook records variable names and safe defaults only. Never paste or record actual token/API-key values in chat, GitHub issues, commits, reports, or this runbook.

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

## 14. Current continuation checkpoint

The current continuation path after the clean `~/YasinEco` re-clone is:

```text
YasinRelay interactive configuration verified
        ↓
local .env verified (no secrets recorded)
        ↓
YasinHub control path
        ↓
Start → real PID/process identity verification
        ↓
real publish acceptance
        ↓
Stop / Restart → PID lifecycle verification
        ↓
PWA browser visual acceptance
        ↓
final regression / Issue #174 closure evidence
```

The discovery of `configure_interactively()` is now recorded here so the next operator/session does not need to rediscover the configuration path. Do not treat this source inspection itself as runtime acceptance; runtime claims still require runtime evidence.

## 15. Hub status checkpoint — 2026-09-05

On the clean `~/YasinEco` clone, with `YASIN_ECOSYSTEM_ROOT="$HOME/YasinEco"`, the canonical Hub status command was executed:

```text
PYTHONPATH=. python -m yasinhub.cli status
```

Observed status:

- `yasinrelay`: **FAILED**; last recorded run was unsuccessful with process exit code 1.
- `yasin-agent`: **IDLE/observed running** with a successful last observation.
- `yasin-ai`: **IDLE** with a prior stopped result.
- Other registered services were idle with no report.

This is a persisted Hub status snapshot, not proof that Relay is currently running or currently failing. The next acceptance operation is a targeted Hub-managed `start yasinrelay`, followed by direct status/PID evidence.

### 15.1 Canonical targeted start command

YasinHub's CLI explicitly supports:

```text
PYTHONPATH=. python -m yasinhub.cli start yasinrelay
```

The command selects the registered `yasinrelay` service and calls the Hub `start_service()` lifecycle path. It must be preferred over manually executing the Relay launcher. 

After a successful start, acceptance requires a subsequent Hub status/PID verification and process-identity evidence; the CLI's success message alone is not sufficient.
