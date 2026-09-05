# Yasin Ecosystem Startup Runbook

## Scope

This runbook is the operational entry point for the canonical Termux deployment. It intentionally contains no credentials or secret values.

## Canonical order

```text
Yasin-AI / supporting runtime
        ↓
Yasin-Agent / domain services
        ↓
YasinHub
        ↓
PWA / YasinCLI / approved clients
```

**Lifecycle authority:** YasinHub. Clients request operations through Hub and must use Hub's authoritative result/state.

## Before startup

1. Install repositories under the canonical `$HOME/yasineco/<REPO>` layout.
2. Ensure each project uses its documented virtual environment and entrypoint.
3. Configure required local environment values using the project's safe configuration procedure.
4. Keep credentials local, permission-restricted, and excluded from Git.
5. Run the relevant project doctor/health checks.

## Hub lifecycle

Use the canonical YasinHub control surface for:

- `status`
- `start <service>`
- `stop <service>`
- `restart <service>`
- `health` / diagnostics

A start is successful only when Hub verifies the real process/PID and authoritative health state. A stop is successful only when the process is confirmed terminated. Restart must result in a new valid PID when the service creates a new process.

## Relay publishing gate

Do not claim a real publish until valid operator configuration is present and the actual downstream publish is observed. An empty `SOURCE_CHANNELS` configuration must fail closed rather than being represented as a successful running publisher.

## PWA

The PWA is a control/observability client of Hub. Backend/API verification is separate from visual acceptance. A visual PASS requires a real browser/mobile viewport.

## Recovery

If a service fails to start:

1. Read Hub's authoritative failure state and diagnostic output.
2. Inspect the service's own logs/health endpoint.
3. Correct configuration or dependency issues.
4. Retry through Hub.
5. Confirm real PID/process state and health after retry.

Never manually manufacture PID/state files to represent a running service.

## Evidence

Final ecosystem acceptance evidence is recorded in `docs/operations/FINAL_ECOSYSTEM_ACCEPTANCE_ISSUE_174.md` and the detailed checkpoint reports in `Yasin-Operations`.
