# Yasin Ecosystem — Startup Runbook

Canonical operational documentation for Yasin Ecosystem devices on Termux/Android.

## Table of Contents

1. [Canonical Root and Repository Layout](#1-canonical-root-and-repository-layout)
2. [Existing Device → Sync to Latest Main → Restore Runtime → Verify → Start Hub](#2-existing-device--sync-to-latest-main--restore-runtime--verify--start-hub)
3. [YasinHub Canonical Startup](#3-yasinhub-canonical-startup)
4. [Runtime Verification](#4-runtime-verification)
5. [PWA and Dashboard](#5-pwa-and-dashboard)
6. [Service Lifecycle — Hub-Authoritative](#6-service-lifecycle--hub-authoritative)
7. [Secret and Configuration Preservation](#7-secret-and-configuration-preservation)
8. [Quick Reference Checklist](#8-quick-reference-checklist)

---

## 1. Canonical Root and Repository Layout

### Canonical root

The canonical root for all Yasin Ecosystem repositories on Termux/Android is:

```text
~/YasinEco/
```

This is the **contract-defined canonical path** used by the startup runbook, the existing YasinHub `STARTUP_RUNBOOK.md`, and the operational documentation.

**Important distinction**: A separate document, [`docs/operations/TERMUX_CANONICAL_PROJECT_LAYOUT.md`](operations/TERMUX_CANONICAL_PROJECT_LAYOUT.md), defines a local filesystem convention of `~/yasineco/` (lowercase). That document governs fresh bootstrap and reinstall commands. This runbook uses `~/YasinEco/` (uppercase) as the canonical contract path for **existing-device synchronization and runtime operations**. If your local clone directory differs, see the migration note in Section 2.

### Canonical repositories

All of the following repositories are canonical members of the Yasin Ecosystem and must be covered by the sync procedure:

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

### Target branch

All sync operations target `origin/main`. This is the canonical integration branch for the ecosystem.

```text
canonical remote: https://github.com/yusi20006-max
canonical branch: origin/main
```

---

## 2. Existing Device → Sync to Latest Main → Restore Runtime → Verify → Start Hub

This procedure brings an **already-installed** Yasin ecosystem checkout to the latest `origin/main` state, restores the expected runtime environment, verifies the Hub, and starts it through the canonical path.

### 2.1 Pre-sync: Assess local state

Before any destructive operation, assess the current state of every repository:

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

### 2.2 Identify tracked and untracked changes

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

### 2.3 Warnings for destructive operations

> ⚠️ **CRITICAL WARNING**: The following commands will **permanently destroy** local tracked changes and untracked files. They must **only** be run after confirming that no needed work is at risk.
>
> - `git reset --hard origin/main` — discards all local tracked modifications and resets HEAD to `origin/main`
> - `git clean -fd` — removes all untracked files and directories
>
> **Never run these silently. Always announce them explicitly before execution.**
>
> **Secrets safety**: `git reset --hard` and `git clean -fd` never touch files outside the repository working tree. Configuration files in `~/.yasinhub/`, `~/.config/`, and other system locations are **not affected**. Secret values are **never** printed, logged, or committed by these commands.

### 2.4 Sync procedure per repository

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

> ⚠️ `git reset --hard origin/main` discards local tracked changes. See Section 2.2 and 2.3 above.

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

### 2.5 Post-sync: Restore runtime environment

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

### 2.6 Verify Hub revision and status after sync

```bash
cd ~/YasinEco/YasinHub
echo "YasinHub HEAD: $(git rev-parse HEAD)"
echo "YasinHub origin/main: $(git rev-parse origin/main)"
echo "YasinHub branch: $(git branch --show-current)"

# Verify the startup module exists (required for canonical startup)
test -f yasinhub/startup.py && echo "yasinhub.startup module: FOUND" || echo "yasinhub.startup module: MISSING"
```

### 2.7 Start Hub through canonical path

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

### 2.8 Post-startup verification

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

## 3. YasinHub Canonical Startup

### 3.1 The canonical startup path

```bash
cd ~/YasinEco/YasinHub
python -m yasinhub.startup --port 7000
```

This is the **only** canonical startup entry point. There is no `serve` command and no alternative startup path.

### 3.2 The non-canonical alternative (diagnostics only)

`python -m yasinhub.api.server` exists for diagnostics only. It is **not** the canonical startup path and should not be used in procedure documentation or operational runbooks as the primary startup method.

### 3.3 Runtime environment restoration

After a sync operation, the runtime environment must be re-established:

```bash
cd ~/YasinEco/YasinHub
source .venv/bin/activate
pip install -e .
python -c "import yasinhub; print('YasinHub version:', yasinhub.__version__)"
```

### 3.4 Hub-authoritative lifecycle

All service lifecycle operations must go through YasinHub:

```bash
# Start a service
python -m yasinhub.cli start yasin-agent

# Stop a service
python -m yasinhub.cli stop yasin-agent

# Restart a service
python -m yasinhub.cli restart yasin-agent

# Check status
python -m yasinhub.cli status

# Health diagnostics
python -m yasinhub.cli doctor
```

**Runbook must not:**
- Introduce a second lifecycle controller
- Recommend `kill -9` as a normal path
- Bypass YasinHub for service management
- Create a separate Control Plane

---

## 4. Runtime Verification

After the sync-and-startup procedure, verify the following on the actual Termux/Android device:

### 4.1 Repository sync verification

```bash
# For each canonical repo
cd ~/YasinEco/$REPO
echo "$REPO: HEAD=$(git rev-parse HEAD) origin/main=$(git rev-parse origin/main)"
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" && echo "PASS" || echo "FAIL"
```

### 4.2 Hub process verification

```bash
# Confirm the Hub process exists
ps aux | grep yasinhub.api.server | grep -v grep

# Confirm the port is listening
python -c "import socket; s=socket.socket(); s.settimeout(2); result=s.connect_ex(('127.0.0.1',7000)); print('Port 7000:', 'OPEN' if result==0 else 'CLOSED'); s.close()"
```

### 4.3 API endpoint verification

```bash
# Health endpoint
curl -s http://127.0.0.1:7000/api/health

# Version endpoint
curl -s http://127.0.0.1:7000/api/version

# Services endpoint
curl -s http://127.0.0.1:7000/api/services
```

### 4.4 YasinHub CLI verification

```bash
python -m yasinhub.cli status
python -m yasinhub.cli doctor
```

### 4.5 Evidence policy

- Use **real runtime output** from `curl`, `ps`, `git`, and `python -m yasinhub.cli` as verification evidence
- Do **not** report documentation inspection as runtime PASS
- If an endpoint does not respond, report it as NOT VERIFIED, not PASS

---

## 5. PWA and Dashboard

### 5.1 Canonical PWA endpoint

```text
http://127.0.0.1:7000/dashboard/
```

### 5.2 PWA refresh/reopen guidance

After any sync or restart operation:

1. If the frontend or service worker changed during the sync, a **manual refresh** is required
2. Open the browser to `http://127.0.0.1:7000/dashboard/`
3. **Force refresh** (`Ctrl+Shift+R` or `Cmd+Shift+R`) to bypass cached service workers
4. If the dashboard does not update, **close and reopen** the browser tab or window
5. Do **not** claim visual PWA acceptance without browser evidence

> **Static documentation alone is not runtime acceptance.** Dashboard rendering from cache is not evidence of a healthy Hub.

---

## 6. Service Lifecycle — Hub-Authoritative

### 6.1 Control Plane architecture

```text
USER / OPERATOR
       │
       ▼
  YasinCLI
       │
       ▼
  YasinHub          ← sole lifecycle/PID authority
       │
       ▼
  Runit / Service   ← supervised by runit, observed by Hub
       │
       ▼
  Applications
```

YasinHub is the **only** lifecycle and PID authority. All service operations must route through YasinHub.

### 6.2 Lifecycle commands (through Hub only)

```bash
python -m yasinhub.cli start <service>
python -m yasinhub.cli stop <service>
python -m yasinhub.cli restart <service>
python -m yasinhub.cli status
python -m yasinhub.cli doctor
```

### 6.3 Prohibited patterns

The Runbook must **never** recommend:

- Direct `kill -9` as a normal lifecycle operation
- A second Control Plane or lifecycle manager
- Bypassing YasinHub for service management
- Using `serve` or any nonexistent command for YasinHub startup

---

## 7. Secret and Configuration Preservation

### 7.1 Rule: Secrets are never printed, logged, or committed

```bash
# NEVER do this in any documentation or verification:
echo "TOKEN=secretvalue"          # ✗ NEVER
cat ~/.yasinhub/yasin-agent.token # ✗ NEVER in docs
git add .env                      # ✗ NEVER
```

### 7.2 Safe inspection

If inspection is needed, show **metadata only**, never secret values:

```bash
# Safe: check if token file exists (metadata)
ls -la ~/.yasinhub/yasin-agent.token

# Safe: check file permissions (metadata)
stat ~/.yasinhub/yasin-agent.token

# NEVER: cat the file contents or print its value
```

### 7.3 Protected files

The following files and directories contain secrets or configuration and must **never** be overwritten by `git reset --hard` or `git clean -fd` because they are outside the repository working tree:

- `~/.yasinhub/` — token files, config, PID files, logs
- `~/.config/` — application configuration
- Project `config.yaml` if located outside the repository

**However**, if a `.env` file or credential file exists **inside** a repository directory, `git reset --hard` **will** overwrite it. Always check before running destructive commands (Section 2.2).

### 7.4 git staging protection

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

## 8. Quick Reference Checklist

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

## Appendix: Common Issues

### "Address already in use" on port 7000

Another process occupies port 7000. Use `python -m yasinhub.startup` which handles this gracefully via preflight. If it refuses with FAIL CLOSED, investigate the occupying process identity — do not force-kill.

### `yasinhub.startup` module not found

Ensure YasinHub repository is synced to `origin/main` where `yasinhub/startup.py` exists. Verify with `ls ~/YasinEco/YasinHub/yasinhub/startup.py`.

### `/api/health` not responding

Confirm the Hub process is running (`ps aux | grep yasinhub.api.server`). Check the startup log at `~/.yasinhub/logs/yasinhub.log`. Use `python -m yasinhub.cli doctor` for diagnostics.

### PWA shows stale content

Force refresh (`Ctrl+Shift+R`) and close/reopen the browser tab. Cached service workers must be bypassed after sync.
