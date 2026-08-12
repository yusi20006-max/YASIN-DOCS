# YasinPress Rewrite

> Status: **🟡 actively being hardened**
> Repository: `yusi20006-max/YasinPress-Rewrite-`
> Default branch: `main`
> Current release: `1.0.0`

> **Update (2026-08-10):** A fresh Termux installation on Python `3.14.6` succeeded. `pytest` was installed separately and all `114` tests passed. CLI version/status/health/configuration all returned successfully. BBC Persian RSS was independently verified with HTTP `200` and valid current XML. `YasinPress CI #68` on commit `13b8381` was reported successful. A previous Eitaa smoke test succeeded, but its credential was subsequently revoked, so live Eitaa delivery still requires a fresh credential and end-to-end verification.

## Role

YasinPress Rewrite is a Python news-automation application responsible for the application-level pipeline that collects RSS content, processes articles, assigns category/priority/breaking state, optionally uses an AI provider, and publishes through configured destinations such as Eitaa, PWA JSON Feed and RSS.

It is an **application/domain pipeline**, not the system-wide Yasin control plane. Cross-project orchestration and ecosystem-level coordination remain outside this repository.

## Verified implementation

The repository implements:

- RSS feed fetching and source management
- feed parsing, filtering and duplicate detection
- article validation and formatting
- category, priority and breaking-state processing
- AI provider abstraction
- publisher abstraction and destination adapters
- SQLite repositories, migrations and transactional persistence
- priority queue, retry policy and scheduler
- cache, health checks, metrics, diagnostics and statistics
- configuration from defaults and environment variables
- REST-style routing and CLI
- persistent JSON Feed output for the PWA
- persistent RSS 2.0 output

## Runtime verification — Termux

Fresh clone/install sequence used:

```bash
cd ~
rm -rf YasinPress-Rewrite-
git clone https://github.com/yusi20006-max/YasinPress-Rewrite-.git
cd YasinPress-Rewrite-

python3 --version
python3 -m venv .venv
source .venv/bin/activate

python --version
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install pytest
python -m pytest -q

python -m yasinpress.cli.main --help
```

Observed on the tested device:

```text
Python 3.14.6
114 passed in 3.84s
YasinPress version: 1.0.0
database: ok
configuration: ok
```

The clean install therefore works on the tested Termux/Python 3.14 environment, while the project metadata still declares Python `>=3.13`.

## Normal CLI operation

After activation:

```bash
cd ~/YasinPress-Rewrite-
source .venv/bin/activate

yasinpress version
yasinpress status
yasinpress health
yasinpress config
yasinpress run
```

`yasinpress run` is the long-running application mode. It loads RSS feeds, processes eligible articles, persists them, and publishes to configured destinations. It should remain running until interrupted.

## RSS verification

The configured feed variable was observed as:

```text
YASINPRESS_FEEDS=https://feeds.bbci.co.uk/persian/rss.xml
```

An independent HTTPX request returned:

```text
STATUS: 200
CONTENT-TYPE: text/xml; charset=utf-8
```

and valid BBC Persian RSS XML containing current articles. Therefore the previous lack of channel output was **not caused by the BBC RSS endpoint being unavailable**.

## Runtime hardening completed

Two runtime issues were identified and corrected in the repository:

1. Worker jobs now retain the return value of their handler in `Job.result`. This allows the runtime layer to inspect the actual `ApplicationReport` after feed processing.
2. The runtime status check was using the nonexistent `job.state` attribute instead of `job.status`. After a successful processing job, that could raise an exception and terminate the long-running loop immediately after the first cycle.

The PWA client was also hardened to keep the latest successfully loaded JSON Feed in browser storage and display it when the network is unavailable.

These changes are intended to make the RSS → processing → PWA/RSS path persistent rather than merely passing isolated unit tests.

## Publishing verification

A previous manual Eitaa smoke test was reported as successful before the publishing token was revoked. The current source tree contains the Eitaa publisher implementation and publishing tests.

The current Eitaa credential must **not** be reconstructed from repository history or documentation. A fresh credential is required for a new live test. No credential value should ever be written into YASIN-DOCS or the YasinPress repository.

## Current operational boundary

### Verified

- repository clone
- Python virtual environment
- editable package installation
- 114-test Termux run
- CLI entrypoint
- version reporting
- database status check
- health check
- configuration check
- direct BBC Persian RSS reachability
- PWA/RSS publisher implementation exists

### Requires fresh live verification

- complete `yasinpress run` feed-to-destination flow after the runtime fixes
- live Eitaa publishing after credential replacement
- production AI provider execution
- long-running scheduler behavior after the runtime fixes
- deployed PWA/RSS hosting and browser installation

## Architecture position in Yasin

```text
                    Yasin ecosystem
                           │
                    ┌──────┴──────┐
                    │             │
               Control /      Application
               orchestration    pipelines
                    │             │
                    │       YasinPress Rewrite
                    │             │
                    │       RSS → Process
                    │       → AI (optional)
                    │       → Persistence
                    │       → PWA JSON Feed
                    │       → RSS 2.0
                    │       → Eitaa (optional)
                    │
                    └─────────────┘
```

The exact runtime relationship between YasinPress Rewrite and other Yasin content projects must remain evidence-based. It should not be assumed that YasinPress Rewrite is interchangeable with YasinFeed or YasinRelay merely because their domains overlap.

## Evidence policy

This record intentionally separates:

- **verified implementation** — supported by repository files or executed tests;
- **runtime verification** — supported by an actual local execution;
- **historical verification** — reported from an earlier successful test;
- **pending verification** — behavior that still needs a fresh live test.

Planned behavior must not be presented as current implementation without evidence.

## Next verification target

The next YasinPress verification target is a controlled end-to-end run after the runtime fixes:

1. start with the already verified RSS configuration;
2. run `yasinpress run`;
3. confirm the first feed cycle executes and the process remains alive;
4. inspect the generated PWA JSON Feed and RSS XML files;
5. only then retest Eitaa with a fresh credential;
6. record the resulting evidence here.
