# YASIN-DOCS

## Yasin Ecosystem Documentation Hub

YASIN-DOCS is the canonical documentation and architecture repository for the Yasin Ecosystem.

## Start Here

1. [Canonical Ecosystem Architecture](docs/architecture/YASIN_ECOSYSTEM_CANONICAL_ARCHITECTURE_V1.md)
2. [Dependency Matrix](docs/architecture/ECOSYSTEM_DEPENDENCY_MATRIX_V1.md)
3. [Termux-First Compatibility Contract](docs/compatibility/TERMUX_FIRST_COMPATIBILITY_CONTRACT_V1.md)
4. [Yasin Ecosystem Startup Runbook](docs/STARTUP_RUNBOOK.md)
5. [Termux Canonical Project Layout](docs/operations/TERMUX_CANONICAL_PROJECT_LAYOUT.md)
6. [Real Publish Acceptance Record — 2026-09-06](docs/operations/REAL_PUBLISH_ACCEPTANCE_2026-09-06.md)

## Canonical startup rule

For Termux/Android ARM64, YasinHub is started through its self-healing startup launcher. The canonical ecosystem root is `~/YasinEco` and YasinHub owns dedicated HTTP port `7000`.

### Sync + Start YasinHub

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

Startup behavior:

- `7000` free → start YasinHub.
- Existing verified YasinHub on `7000` → graceful stop, wait for process/port release, then start a new instance.
- Foreign or unverified owner → fail closed; never kill the process.
- Normal path uses graceful termination, not blind `kill -9`.
- Success requires real PID/process identity, listening port and health verification.
- The launcher is non-interactive and Termux/Android ARM64 compatible.

A successful launcher may return to the shell after starting the Hub. The authoritative runtime check is:

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

PWA:

```text
http://127.0.0.1:7000/dashboard/
```

Version/build:

```bash
curl -sS http://127.0.0.1:7000/api/version
```

The full operational procedure, security rules, lifecycle authority and acceptance evidence remain in `docs/STARTUP_RUNBOOK.md`.

## Canonical architecture

```text
USER / OPERATOR
      ↓
   YasinCLI
      ↓
   YasinHub
      ↓
Yasin-Core / Yasin-Agent / Applications
      ↓
   Yasin-AI
```

YasinHub is the ecosystem control and observability plane. Yasin-AI is the canonical shared AI capability platform.

## Repository Map

| Repository | Role |
|---|---|
| `Yasin-Core` | Runtime and SDK foundation |
| `Yasin-Agent` | Agent/workflow execution |
| `Yasin-AI` | Canonical AI platform |
| `YasinHub` | Ecosystem control and observability plane |
| `YasinCLI` | Unified user-facing CLI and ecosystem orchestration |
| `YasinRelay` | Telegram/content relay and publishing pipeline |
| `YasinFeed` | General content aggregation/processing/publishing |
| `YasinPress` | Specialized Persian-news publishing |
| `YASIN-DOCS` | Canonical ecosystem documentation |

## Evidence Policy

YASIN-DOCS uses four evidence states: Confirmed, Target, Proposed, and Unresolved. Never convert a target or proposed relationship into a confirmed runtime dependency without implementation evidence.

## Change Governance

Cross-project architectural changes should update affected architecture documentation, canonical architecture/dependency documents where applicable, ADRs for intentional decisions, and public API/compatibility documentation when contracts change.

Individual repositories remain the source of truth for implementation. YASIN-DOCS is the source of truth for system-level architecture and documented decisions.

## Termux-first rule

All active Yasin runtime repositories use the canonical ecosystem root `~/YasinEco`. Termux/Android is a first-class runtime target. Runtime compatibility, process lifecycle, service entrypoints and health must be validated on the target environment rather than inferred from package metadata.

## Status

Operational startup is standardized around the YasinHub self-healing launcher on dedicated port `7000`. Real publish acceptance is recorded separately; PWA visual acceptance remains a distinct evidence gate.
