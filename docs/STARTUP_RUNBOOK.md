# Yasin Ecosystem Startup Runbook

**Status:** Canonical operational runbook
**Platform:** Android / Termux / ARM64
**Canonical root:** `~/YasinEco`
**YasinHub dedicated port:** `7000`
**Last verified:** 2026-09-11

## 1. Authority

YasinHub is the sole Control Plane and lifecycle/PID authority. The PWA requests lifecycle operations through YasinHub. Do not create a second Control Plane or maintain an independent PID authority.

Canonical flow:

```text
PWA → YasinHub → Yasin-Agent → YasinRelay
                  ↓
               Yasin-AI
```

### 1.5 Canonical repositories

All of the following repositories are canonical members of the Yasin Ecosystem and must be covered by any sync procedure:

| Repository | Role |
|---|---|
| `Yasin-Core` | Runtime and SDK foundation |
| `Yasin-Agent` | Agent/workflow execution |
| `Yasin-AI` | Canonical AI platform |
| `YasinHub` | Ecosystem control and observability plane |
| `YasinCLI` | Unified user-facing CLI and ecosystem orchestration |
| `YasinRelay` | Telegram/content relay and publishing pipeline |
| `YasinFeed` | General content aggregation/processing/publishing |
| `YasinPress` | Specialized Persian-news publishing automation |
| `YASIN-DOCS` | Canonical ecosystem documentation |

All sync operations target `origin/main` from the canonical remote `https://github.com/yusi20006-max`.

### 1.6 Canonical root path

The canonical root for all Yasin Ecosystem repositories on Termux/Android is `~/YasinEco/`. This is the contract-defined canonical path used by the startup runbook.

A separate document, [`docs/operations/TERMUX_CANONICAL_PROJECT_LAYOUT.md`](operations/TERMUX_CANONICAL_PROJECT_LAYOUT.md), defines a local filesystem convention of `~/yasineco/` (lowercase) for fresh bootstrap and reinstall commands. This runbook uses `~/YasinEco/` (uppercase) as the canonical contract path for existing-device synchronization and runtime operations. If your local clone directory differs, see Section 2 for migration guidance.

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
| OpenFeed | 7006 |
| YasinRelay | portless unless a proven HTTP runtime exists |
| Yasin-AI | portless unless a proven HTTP runtime exists |
| YasinPress | portless unless a proven HTTP runtime exists |
| Yasin-Coder | portless unless a proven HTTP runtime exists |

OpenFeed is an independent repository/runtime and is **not** a YasinHub or YasinRelay dependency. Its canonical local PWA address is:

```text
http://127.0.0.1:7006/
```

The OpenFeed runtime defaults to port `7006` and accepts `OPENFEED_PORT` for an explicitly overridden local port.

### 6.1 OpenFeed — canonical Termux/runit startup

OpenFeed is independently managed from the YasinHub lifecycle because it is an independent repository/runtime. On Termux, use `runit` for its persistent local process; do not start a second copy with `./openfeed` while the runit service is active.

Service directory:

```text
~/.local/service/openfeed
```

The service `run` entrypoint is:

```sh
#!/data/data/com.termux/files/usr/bin/sh
cd "$HOME/yasineco/Openfeed"
exec ./openfeed
```

Canonical startup prerequisites:

1. The repository must exist at `~/yasineco/Openfeed`.
2. The `openfeed` binary must be built at `~/yasineco/Openfeed/openfeed`.
3. The service directory must contain an executable `run` file.
4. `runsvdir` must supervise `~/.local/service`.
5. Only one OpenFeed instance may own port `7006`.

Canonical setup/start commands on Termux:

```bash
cd ~/yasineco/Openfeed

mkdir -p ~/.local/service/openfeed

cat > ~/.local/service/openfeed/run <<'EOF'
#!/data/data/com.termux/files/usr/bin/sh
cd "$HOME/yasineco/Openfeed"
exec ./openfeed
EOF

chmod +x ~/.local/service/openfeed/run

mkdir -p ~/.local/service
nohup runsvdir "$HOME/.local/service" > "$HOME/.local/service/runsvdir.log" 2>&1 &

sleep 2
sv up "$HOME/.local/service/openfeed"
sv status "$HOME/.local/service/openfeed"
```

If an older manually started `./openfeed` is already using port `7006`, stop that old process before enabling the runit service. Never run a manual `./openfeed` alongside the supervised service.

Canonical runtime verification:

```bash
sv status ~/.local/service/openfeed
curl -I http://127.0.0.1:7006/
pgrep -af openfeed
```

Acceptance requires a `run:` status from `sv`, an HTTP response from port `7006`, and exactly one active OpenFeed process owned by the runit service.

Control commands:

```bash
sv up ~/.local/service/openfeed
sv down ~/.local/service/openfeed
sv restart ~/.local/service/openfeed
sv status ~/.local/service/openfeed
```

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

---

## 15. Existing Device — Sync to Latest Main: Detailed Procedure

This procedure brings an already-installed Yasin ecosystem checkout to the latest `origin/main` state, restores the expected runtime environment, verifies the Hub, and starts it through the canonical path.

### 15.1 Pre-sync: Assess local state

Before any destructive operation, assess the current state of every canonical repository:

```bash
for repo in Yasin-Core Yasin-Agent Yasin-AI YasinHub YasinCLI YasinRelay YasinFeed YasinPress YASIN-DOCS; do
  echo "=== $repo ==="
  cd ~/YasinEco/$repo
  echo "--- Branch ---"
  git branch --show-current
  echo "--- Status ---"
  git status --short
  echo "--- Last commit ---"
  git log --oneline -1
  echo "--- Fetch ---"
  git fetch origin 2>&1 | tail -1
  echo "--- origin/main HEAD ---"
  git rev-parse origin/main 2>/dev/null
  echo ""
done
```

This step is **read-only**. No files are modified.

### 15.2 Identify tracked and untracked changes

Before any destructive operation, identify what will be affected:

```bash
# For each repo, show tracked changes that will be lost
cd ~/YasinEco/$repo
git diff --stat HEAD          # tracked modifications
git diff --cached --stat HEAD # staged changes
git status --short            # all changes including untracked
```

**If you have local tracked changes or untracked files that you need to preserve:**

1. **Stash or back them up manually** before proceeding:
   ```bash
   cd ~/YasinEco/$repo
   git stash push -m "backup-$(date +%Y%m%d-%H%M%S)"
   ```
   Or copy specific files to a safe location outside the repo.

2. **Configuration files**: `.env`, token files, `config.yaml`, and credential files are typically located in `~/.yasinhub/` or project-specific config directories. These are **NOT** tracked by git and will survive `git reset --hard`. However, **always verify** they are not inside a repository directory before running destructive commands.

3. **Untracked runtime files**: If you have untracked files in the repository that you need to keep, copy them before `git clean -fd`.

### 15.3 Warnings for destructive operations

> ⚠️ **CRITICAL WARNING**: The following commands will **permanently destroy** local tracked changes and untracked files. They must **only** be run after confirming that no needed work is at risk.
>
> - `git reset --hard origin/main` — discards all local tracked modifications and resets HEAD to `origin/main`
> - `git clean -fd` — removes all untracked files and directories
>
> **Never run these silently. Always announce them explicitly before execution.**
>
> **Secrets safety**: `git reset --hard` and `git clean -fd` never touch files outside the repository working tree. Configuration files in `~/.yasinhub/`, `~/.config/`, and other system locations are **not affected**. Secret values are **never** printed, logged, or committed by these commands.

### 15.4 Sync procedure per repository

For each canonical repository, execute the following:

#### Step A — Enter the repository directory

```bash
cd ~/YasinEco/$REPO
```

#### Step B — Fetch from origin

```bash
git fetch origin
```

#### Step C — Verify origin/main exists and record revision

```bash
echo "origin/main SHA: $(git rev-parse origin/main)"
```

#### Step D — Sync to origin/main

**Safe sync (recommended for most cases):**

If you have **no** local changes that need preservation:

```bash
git checkout main 2>/dev/null || git checkout -b main origin/main
git reset --hard origin/main
```

> ⚠️ `git reset --hard origin/main` discards local tracked changes. See Section 15.2 and 15.3 above.

**Destructive runtime-mirror sync (only for disposable/runtime mirrors):**

If the repository is a **disposable runtime mirror** (i.e., you intentionally want to wipe all local work and mirror `origin/main` exactly):

```bash
# 1. Announce the destructive operation
echo "WARNING: This will DESTROY all local tracked and untracked changes in $REPO"

# 2. Confirm no needed secrets/config files are inside the repo
#    (Check ~/.yasinhub/ and other system paths separately)

# 3. Reset tracked files
git reset --hard origin/main

# 4. Remove untracked files
git clean -fd
```

> ⚠️ `git clean -fd` removes **all** untracked files and directories. This includes build artifacts, logs, and any files not committed. **Only run this after confirming no needed untracked files exist.**

#### Step E — Verify the sync

```bash
echo "HEAD SHA:    $(git rev-parse HEAD)"
echo "origin/main: $(git rev-parse origin/main)"
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" && echo "SYNC VERIFIED: HEAD matches origin/main" || echo "SYNC FAILED"
```

### 15.5 Post-sync: Restore runtime environment

After all repositories are synced, restore the expected YasinHub runtime environment:

```bash
# 1. Ensure Python virtual environment exists
cd ~/YasinEco/YasinHub
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# 2. Activate and reinstall dependencies
source .venv/bin/activate
pip install -e .
pip install pyyaml rich

# 3. Verify yasinhub module is importable
python -c "import yasinhub; print(yasinhub.__version__)"
```

### 15.6 Verify Hub revision and status after sync

```bash
cd ~/YasinEco/YasinHub
echo "YasinHub HEAD: $(git rev-parse HEAD)"
echo "YasinHub origin/main: $(git rev-parse origin/main)"
echo "YasinHub branch: $(git branch --show-current)"

# Verify the startup module exists (required for canonical startup)
test -f yasinhub/startup.py && echo "yasinhub.startup module: FOUND" || echo "yasinhub.startup module: MISSING"
```

### 15.7 Start Hub through canonical path

**The canonical startup command is `python -m yasinhub.startup`.** This is the official self-healing launcher defined in Issue #180.

```bash
cd ~/YasinEco/YasinHub
python -m yasinhub.startup --port 7000
```

What this does:
1. **Preflight**: Checks port 7000 for conflicts
2. **Identify**: Verifies if an existing YasinHub process occupies the port
3. **Safely restart**: If a verified YasinHub is running, gracefully stops it via `SIGTERM` (never `kill -9` on the normal path)
4. **Start**: Spawns `python -m yasinhub.api.server`
5. **Verify**: Confirms PID, identity, port ownership, listening, and `/api/health`

> **Never use `kill -9` as a normal path.** The launcher uses `SIGTERM` with a grace period and verifies process death before proceeding. If the launcher refuses (FAIL CLOSED), it means port ownership could not be verified — investigate rather than force-kill.

### 15.8 Post-startup verification

After `python -m yasinhub.startup` completes successfully:

#### Health check

```bash
curl -i http://127.0.0.1:7000/api/health
```

Expected response:
```text
HTTP 200
{"service":"YasinHub","status":"ok"}
```

#### Version check

```bash
curl -i http://127.0.0.1:7000/api/version
```

Expected response includes the canonical PWA version (`1.0.0`) and build identity.

#### Service status

```bash
python -m yasinhub.cli status
python -m yasinhub.cli doctor
```

#### PID verification

```bash
# Confirm the Hub process is running
ps aux | grep yasinhub.api.server | grep -v grep

# Confirm the PID file exists
cat ~/.yasinhub/pids/yasinhub.pid 2>/dev/null || echo "PID file not found (may use runit)"
```

---

## 16. Secret and Configuration Preservation

### 16.1 Rule: Secrets are never printed, logged, or committed

```bash
# NEVER do this in any documentation or verification:
echo "TOKEN=secretvalue"          # ✗ NEVER
cat ~/.yasinhub/yasin-agent.token # ✗ NEVER in docs
git add .env                      # ✗ NEVER
```

### 16.2 Safe inspection

If inspection is needed, show **metadata only**, never secret values:

```bash
# Safe: check if token file exists (metadata)
ls -la ~/.yasinhub/yasin-agent.token

# Safe: check file permissions (metadata)
stat ~/.yasinhub/yasin-agent.token

# NEVER: cat the file contents or print its value
```

### 16.3 Protected files

The following files and directories contain secrets or configuration and must **never** be overwritten by `git reset --hard` or `git clean -fd` because they are outside the repository working tree:

- `~/.yasinhub/` — token files, config, PID files, logs
- `~/.config/` — application configuration
- Project `config.yaml` if located outside the repository

**However**, if a `.env` file or credential file exists **inside** a repository directory, `git reset --hard` **will** overwrite it. Always check before running destructive commands (Section 15.2).

### 16.4 git staging protection

```bash
# Prevent accidental secret commits
git config --global core.excludesfile ~/.gitignore_global
# Add to ~/.gitignore_global:
# .env
# *.token
# *credentials*
# config.yaml
```

---

## 17. Quick Reference Checklist

```text
[ ] cd ~/YasinEco/<REPO> for each canonical repository
[ ] git fetch origin
[ ] origin/main SHA recorded and verified
[ ] Local tracked changes assessed and backed up if needed
[ ] Untracked files assessed and preserved if needed
[ ] Destructive warnings announced before git reset --hard or git clean -fd
[ ] git reset --hard origin/main executed (if applicable)
[ ] git clean -fd executed (if applicable, with explicit warning)
[ ] HEAD matches origin/main verified for each repo
[ ] Runtime environment restored (.venv, pip install -e .)
[ ] yasinhub.startup module verified present
[ ] python -m yasinhub.startup --port 7000 executed
[ ] GET /api/health = 200 verified
[ ] GET /api/version = valid response verified
[ ] GET /api/services = 200 verified
[ ] python -m yasinhub.cli status verified
[ ] python -m yasinhub.cli doctor verified
[ ] PWA dashboard accessible at http://127.0.0.1:7000/dashboard/
[ ] PWA refresh/reopen guidance applied if frontend changed
[ ] Service lifecycle confirmed Hub-authoritative
[ ] No secrets printed, logged, or committed
[ ] No serve command used
[ ] No kill -9 used as normal path
```

---

## 18. Common Issues

### "Address already in use" on port 7000

Another process occupies port 7000. Use `python -m yasinhub.startup` which handles this gracefully via preflight. If it refuses with FAIL CLOSED, investigate the occupying process identity — do not force-kill.

### `yasinhub.startup` module not found

Ensure YasinHub repository is synced to `origin/main` where `yasinhub/startup.py` exists. Verify with `ls ~/YasinEco/YasinHub/yasinhub/startup.py`.

### `/api/health` not responding

Confirm the Hub process is running (`ps aux | grep yasinhub.api.server`). Check the startup log at `~/.yasinhub/logs/yasinhub.log`. Use `python -m yasinhub.cli doctor` for diagnostics.

### PWA shows stale content

Force refresh (`Ctrl+Shift+R`) and close/reopen the browser tab. Cached service workers must be bypassed after sync.

### `git reset --hard` would overwrite local config

If a `.env` or credential file exists inside a repository directory, back it up before running `git reset --hard`. Copy it to `~/.yasinhub/` or another location outside the repository.
