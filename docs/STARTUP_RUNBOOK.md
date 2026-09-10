# Yasin Ecosystem Startup Runbook

**Status:** Canonical operational runbook
**Platform:** Android / Termux / ARM64
**Canonical root:** `~/YasinEco`
**YasinHub dedicated port:** `7000`
**Last verified:** 2026-09-10

## 1. Authority

YasinHub is the sole Control Plane and lifecycle/PID authority. The PWA requests lifecycle operations through YasinHub. Do not create a second Control Plane or maintain an independent PID authority.

Canonical flow:

```text
PWA → YasinHub → Yasin-Agent → YasinRelay
                  ↓
               Yasin-AI
```

## 2. Canonical YasinHub startup

The official non-interactive Termux/Android startup launcher is:

```bash
cd ~/YasinEco/YasinHub
export YASIN_ECOSYSTEM_ROOT="$HOME/YasinEco"
export PYTHONPATH=.
.venv/bin/python -m yasinhub.startup
```

### 2.1 Sync + Start — standard operator command

When starting from an existing checkout, use:

```bash
cd ~/YasinEco/YasinHub

git fetch origin
git checkout main
git reset --hard origin/main
git clean -fd

export YASIN_ECOSYSTEM_ROOT="$HOME/YasinEco"
export PYTHONPATH=.

.venv/bin/python -m yasinhub.startup
```

`git clean -fd` removes untracked files. Do not use it when local untracked runtime data must be preserved.

### 2.2 Self-healing port behavior

YasinHub owns port `7000`. The startup launcher performs the port preflight itself:

1. If `7000` is free, start YasinHub.
2. If `7000` is occupied by a verified YasinHub process, gracefully stop the old Hub, wait for process death and port release, then start the new Hub.
3. If the owner is foreign, unknown, or cannot be verified as YasinHub, fail closed and **never kill it**.
4. Normal recovery uses graceful termination; blind `kill -9` is not the normal path.
5. After start, the launcher verifies the real runtime state required by the startup contract: process/PID identity, listening port and health.
6. The launcher is non-interactive and designed for Termux/Android ARM64.

## 3. Important Termux behavior

A successful launcher may return to the shell after starting YasinHub. The line:

```text
YasinHub startup ok: action=started pid=<PID> port=7000
```

means the startup action succeeded; it does **not** mean the Hub stopped. The Hub may continue serving in the background.

The authoritative runtime check is:

```bash
curl -sS http://127.0.0.1:7000/api/health
```

Expected:

```json
{
  "service": "YasinHub",
  "status": "ok"
}
```

On the verified Termux run on 2026-09-10, the launcher reported `action=started`, port `7000` was occupied afterward, and `/api/health` returned HTTP 200 with `service=YasinHub` and `status=ok`.

## 4. PWA

After Hub is healthy, open:

```text
http://127.0.0.1:7000/dashboard/
```

Version/build check:

```bash
curl -sS http://127.0.0.1:7000/api/version
```

Do not treat a stale browser cache as current merely because the HTTP server is current; refresh/reopen the PWA after frontend/service-worker changes.

## 5. Service lifecycle

Start/stop/restart services through YasinHub only:

```bash
cd ~/YasinEco/YasinHub
export YASIN_ECOSYSTEM_ROOT="$HOME/YasinEco"
export PYTHONPATH=.

python -m yasinhub.cli status
python -m yasinhub.cli start yasinrelay
python -m yasinhub.cli status
```

For lifecycle acceptance, CLI output alone is insufficient. Verify real process identity, PID liveness and the appropriate health/port contract.

## 6. Port assignments

| Service | Port |
|---|---:|
| YasinHub | 7000 |
| Yasin-Agent | 7002 |
| YasinFeed | 7004 |
| YasinRelay | portless unless a proven HTTP runtime exists |
| Yasin-AI | portless unless a proven HTTP runtime exists |
| YasinPress | portless unless a proven HTTP runtime exists |
| Yasin-Coder | portless unless a proven HTTP runtime exists |

## 7. Canonical Relay launcher

For service/control-plane execution, the canonical Relay launcher is:

```text
.venv/bin/yasinrelay-termux run --schedule --non-interactive
```

The normal interactive configuration path is separate: `run` from a real TTY can invoke `configure_interactively()` and persist runtime settings to the local `.env`. Once configured, YasinHub remains the lifecycle authority.

Never record actual `EITAA_TOKEN`, `AI_API_KEY`, `OPENAI_API_KEY`, or other secret values in documentation, issues, commits, logs or reports.

## 8. Truthful startup and lifecycle rules

A service is RUNNING only after the expected process survives startup and its identity is verified.

- Failed/invalid startup must not retain a stale PID.
- Short-lived processes must not be represented as RUNNING.
- Stop must confirm the old process is dead.
- Restart must confirm the old process is dead before accepting a new verified process.
- Unknown port owners must cause fail-closed behavior.
- `shell=False` is required for lifecycle command execution.

## 9. Health and evidence

Every operational claim must have evidence from command output, tests, API response, process/PID evidence, or browser evidence. Static source inspection alone cannot establish runtime acceptance.

Quick Hub verification:

```bash
curl -sS -i http://127.0.0.1:7000/api/health
```

## 10. Security

- Never kill an unverified process occupying a reserved port.
- Never use blind `kill -9` as the normal startup recovery path.
- Never print or commit credentials.
- Keep `.env` local and preferably `0600`.
- Keep YasinHub as the single lifecycle/PID authority.
- Fail closed when process identity, authorization or required configuration cannot be verified.

## 11. Termux-first rule

Termux/Android ARM64 is a first-class Yasin runtime target. Runtime compatibility, native dependencies, service entrypoints, process lifecycle and health must be verified on the target environment rather than inferred from package metadata.

## 12. Acceptance baseline

Completed acceptance evidence includes real lifecycle verification, YasinHub/PWA backend control-path verification, Termux runtime installation and real publish acceptance. The PWA visual gate remains a separate browser/mobile evidence requirement unless a later evidence record closes it.

## 13. Operations evidence

Canonical real-publish evidence:

```text
Yasin-Operations/reports/active/real-publish-acceptance.md
```

Canonical runbook:

```text
YASIN-DOCS/docs/STARTUP_RUNBOOK.md
```

## 14. Fresh Termux installation note

Fresh-device installation is separate from runtime acceptance. After repositories and virtual environments are installed, use the canonical YasinHub startup command in Section 2. Do not claim lifecycle, publish or PWA visual acceptance from installation alone.
