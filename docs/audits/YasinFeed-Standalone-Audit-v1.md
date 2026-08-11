# YasinFeed — Standalone Runtime Audit v1

- Repository: `yusi20006-max/Yasinfeed`
- Default branch: `main`
- Current declared version: `1.0.0`
- Audit status: **Source-verified baseline**
- Audit date: 2026-08-11

## Executive Result

YasinFeed is documented and implemented as an independent content-processing application. Its repository explicitly assigns it responsibility for collection, processing, storage, rewriting, scheduling, and publishing while excluding orchestration, agent workflows, and CLI ownership from the application itself.

The repository declares a standalone Python package named `yasinfeed`, version `1.0.0`, requiring Python `>=3.8`, with PyYAML and feedparser as runtime dependencies and pytest as a development dependency. A console entry point named `yasinfeed` is declared.

## Confirmed Product Boundary

The repository README states that YasinFeed:

- collects content sources;
- processes and rewrites content;
- prepares content outputs;
- publishes through RSS, PWA-compatible JSON, and Eitaa channels;
- does not function as the ecosystem orchestrator;
- does not implement agent execution workflows;
- does not implement the unified YasinCLI.

This aligns with the ecosystem decision that YasinFeed must remain independently runnable and must not depend on YasinPress at runtime.

## Package / Build Boundary

`pyproject.toml` declares:

- package name: `yasinfeed`;
- version: `1.0.0`;
- Python requirement: `>=3.8`;
- runtime dependencies: `PyYAML>=6.0`, `feedparser`;
- development dependency: `pytest>=7.0.0`;
- CLI entry point: `yasinfeed = yasinfeed.cli.main:main`.

The packaging configuration discovers `yasinfeed*` packages from the repository root.

## Runtime Architecture

The repository README identifies these primary modules:

```text
yasinfeed/
├── api/
├── fetch/
├── models/
├── publisher/
├── rewrite/
├── scheduler/
├── storage/
├── config.py
├── logging.py
└── engine.py
```

The declared responsibility is coherent with a standalone pipeline:

```text
Sources
  ↓
Fetch / Normalize
  ↓
Models / Processing
  ↓
Rewrite / Summarize / Translate
  ↓
Storage
  ↓
Publisher
```

The scheduler is described as the internal cyclic execution layer. It can register a default `fetch_and_process` job that connects fetching, storage, rewriting, and publishing. This is application pipeline automation, not ecosystem orchestration.

## Engine Evidence

`yasinfeed/engine.py` defines `YasinFeedEngine` with explicit lifecycle methods:

```text
initialize()
start()
stop()
```

The engine:

1. loads configuration;
2. configures logging;
3. dynamically loads the application modules;
4. instantiates modules;
5. initializes modules in dependency order;
6. starts modules;
7. waits for shutdown;
8. stops modules in reverse order.

It also defines signal handling for graceful SIGINT/SIGTERM shutdown.

The source therefore supports the conclusion that YasinFeed owns a complete application lifecycle rather than being merely a passive utility library.

## Configuration Boundary

The repository documents a three-layer configuration model:

```text
Defaults
   ↓
YAML config
   ↓
YASINFEED_* environment overrides
```

Nested configuration values use double underscores, for example:

```text
YASINFEED__PUBLISHER__EITAA__ENABLED
YASINFEED__FETCH__INTERVAL_SECONDS
```

The documented configuration model supports independent deployment because application settings can be supplied without another Yasin project being present.

## Installation Boundary

The repository provides a dedicated installation guide for Linux and Termux. It describes:

```bash
git clone https://github.com/yusi20006-max/Yasinfeed.git
cd Yasinfeed
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

It also documents both CLI-based operation and direct foreground execution.

Recommended diagnostics are documented through:

```bash
python -m yasinfeed.cli.main doctor
python -m yasinfeed.cli.main start
python -m yasinfeed.cli.main status
python -m yasinfeed.cli.main stop
```

Foreground execution is documented as:

```bash
python -m yasinfeed.main
```

## Storage Boundary

The installation and production documentation identifies SQLite as the preferred production storage backend and `data/yasinfeed.db` as an example application-local database path.

This supports the ecosystem rule that YasinFeed owns its application state and does not require a shared YasinPress datastore.

## Publishing Boundary

The repository identifies three output families:

- RSS;
- PWA-compatible JSON/API;
- Eitaa.

Publishing is implemented behind a publisher module boundary, allowing delivery channels to be extended without moving orchestration responsibility into Hub or CLI.

## Multi-Source Processing

The README describes source priority/weighting, reliability scoring, failure isolation, and duplicate detection/content merging.

This is important architecturally: source coordination belongs to the YasinFeed application pipeline and is not evidence that YasinFeed should depend on YasinPress.

## Security Boundary

The documented API security layer includes:

- IP-based rate limiting;
- API keys and session tokens;
- role-based permissions;
- security headers.

The production checklist additionally calls for localhost binding by default unless an explicit reverse-proxy/firewall boundary is used.

Sensitive configuration is expected to be masked in diagnostic output.

## Deployment Boundary

The production checklist documents two independent persistence strategies:

- Linux: systemd service;
- Termux: persistent background execution with Termux-specific wake-lock and Android battery-optimization considerations.

This confirms that deployment ownership is inside YasinFeed's own operational boundary, while YasinHub/YasinCLI can remain optional external controllers.

## AI Boundary

YasinFeed's README describes AI rewriting as an extension point and explicitly recommends adapters rather than embedding heavy models directly in the core.

Potential adapters include:

- Ollama;
- OpenAI;
- Claude;
- translation APIs.

No direct dependency on Yasin-AI is established by this audit. The architecture therefore treats Yasin-AI integration as an optional future contract rather than a mandatory runtime dependency.

## Independence From YasinPress

**Confirmed architectural rule:**

```text
YasinFeed ─────X────→ YasinPress
YasinPress ────X────→ YasinFeed
```

YasinFeed has sufficient internal boundaries—fetch, models, rewrite, storage, scheduler, publisher, API, and engine—to execute its own application lifecycle.

YasinPress remains a separate specialized Persian-news application.

Neither project should be imported as the other's runtime foundation.

## What Is Confirmed vs Not Yet Proven

| Item | Status |
|---|---|
| Package exists | CONFIRMED |
| Declared version 1.0.0 | CONFIRMED |
| Python >=3.8 | CONFIRMED |
| Independent CLI entry point | CONFIRMED |
| Independent engine lifecycle | CONFIRMED |
| Independent configuration model | CONFIRMED |
| SQLite application state | CONFIRMED BY DOCUMENTATION |
| RSS/feed collection | CONFIRMED |
| Multi-source processing | CONFIRMED BY DOCUMENTATION |
| Eitaa publisher boundary | CONFIRMED BY DOCUMENTATION |
| PWA output boundary | CONFIRMED BY DOCUMENTATION |
| AI adapter boundary | CONFIRMED BY DOCUMENTATION |
| Direct Yasin-AI dependency | NOT ESTABLISHED |
| Runtime dependency on YasinPress | PROHIBITED / NONE REQUIRED |
| Runtime dependency on YasinHub | NONE REQUIRED |
| Runtime dependency on YasinCLI | NONE REQUIRED |
| Full production deployment verification on current device | NOT YET VERIFIED IN THIS AUDIT |

## Evidence Files Reviewed

- `README.md`
- `pyproject.toml`
- `docs/installation.md`
- `docs/production_checklist.md`
- `yasinfeed/engine.py`

## Next Verification Pass

The next YasinFeed audit should verify source-level evidence for:

1. actual CLI commands and behavior;
2. scheduler implementation and default pipeline registration;
3. fetcher/source registry implementation;
4. storage implementation and schema/migrations;
5. publisher implementations, especially Eitaa/RSS/PWA;
6. rewrite implementation and AI adapter boundaries;
7. test suite and current CI state;
8. actual Termux installation/run behavior;
9. configuration/secrets handling;
10. any hidden imports or package dependencies that could violate standalone operation.

Only after that pass should YasinFeed be marked **fully audited**.
