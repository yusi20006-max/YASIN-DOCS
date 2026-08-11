# YasinPress Rewrite

> Status: **⚠️ CI currently failing on `main` — do not treat as a verified baseline without re-checking**
> Repository: `yusi20006-max/YasinPress-Rewrite-`
> Default branch: `main`
> Current release: `1.0.0`

> **Update (2026-08-12):** The "verified runnable baseline" / "114 passed" claims below are stale. Both `YasinPress CI` and `Python Compatibility` GitHub Actions workflows are currently failing on `main` (confirmed via the Actions API, not just the runtime-verification note further down). An independent local test run (Python 3.12, closest available to the project's declared `>=3.13` — two of the failures below are artifacts of that substitution and not real bugs: `test_runtime_metadata_is_authoritative` and `test_runtime_metadata_matches_release_policy`, which just assert the pyproject string says 3.13) found 6 failures that are **not** Python-version artifacts and look like genuine bugs:
> - `test_orchestrator_is_idempotent_after_success` (fails in both `test_orchestrator_reliability.py` and `test_publishing.py`) — publishing the same article twice returns `success_count == 0` instead of skipping cleanly with a successful idempotent result
> - `test_all_destination_adapters_share_contract` / `test_eitaa_publisher_sends_message` — `EitaaPublisher.render()` no longer includes the article URL in its output
> - `test_startup_allows_custom_feed` — CLI startup test failure
> - `test_dependency_contract.py::test_runtime_and_dependency_sources_are_consistent`
>
> The last 5 commits on `main` were all made within the same minute on 2026-08-11 (`22:54`–`22:56`), and the idempotency failure lines up with the most recent commit message ("show duplicate and hourly publication state"), suggesting this may be an in-progress/uncommitted-fix state rather than a settled regression. Re-verify against the latest `main` before relying on any pass/fail figure in this document, including the ones below.

## Role

YasinPress Rewrite is a Python news-automation application responsible for the application-level pipeline that collects RSS content, processes articles, assigns category/priority/breaking state, optionally uses an AI provider, and publishes through configured destinations such as Eitaa.

It is an **application/domain pipeline**, not the system-wide Yasin control plane. Cross-project orchestration and ecosystem-level coordination remain outside this repository.

## Verified implementation

The repository README documents the following implemented areas:

- RSS feed fetching and source management
- filtering and duplicate detection
- article validation and formatting
- category and priority processing
- AI provider abstraction
- publisher abstraction for Telegram, Eitaa and webhooks
- SQLite repositories, migrations and transactional unit-of-work support
- priority queue, retry policy and scheduler
- cache, health checks, metrics, diagnostics and statistics
- configuration from defaults, JSON, YAML and environment variables
- REST-style routing and CLI

The release notes identify version `1.0.0` as the current foundation release and state that processing, cache, scheduler, API and categorization tests were included in the release verification.

## Runtime verification — 2026-08-11

A fresh clone was installed on Termux with Python `3.14.6`.

The editable installation completed successfully with the repository's current package metadata.

After installing the test dependency separately:

```text
114 passed in 3.84s
```

The CLI was also verified:

```text
yasinpress version  -> 1.0.0
yasinpress status   -> database: ok
yasinpress health   -> database: ok
yasinpress config   -> configuration: ok
```

This establishes that the current repository can be installed and its basic CLI/database/configuration health path works on the tested Termux/Python 3.14 environment, even though the project documentation currently targets Python 3.13.

## Feed verification

The configured shell variable was observed as:

```text
YASINPRESS_FEEDS=https://feeds.bbci.co.uk/persian/rss.xml
```

The RSS endpoint was independently fetched with HTTPX and returned HTTP `200` with valid RSS/XML content and current BBC Persian items.

Important distinction: feed availability was verified independently; successful fetching of the feed does **not** by itself prove that the full `yasinpress run` pipeline will publish an item.

## Publishing verification

A previous manual Eitaa smoke test was reported as successful before the publishing token was revoked. The current source tree contains the Eitaa publisher implementation and publishing tests.

The later runtime investigation found that `yasinpress run` did not result in a visible channel post. The publishing credential had also been revoked during the investigation. Therefore the current documentation must **not** claim that live Eitaa publishing is currently operational until a fresh credential is supplied and a new end-to-end smoke test succeeds.

## Current operational boundary

### Verified working

- repository clone
- Python virtual environment
- editable package installation
- test suite
- CLI entrypoint
- version reporting
- database status check
- health check
- configuration check
- direct RSS endpoint reachability

### Requires fresh live verification

- complete `yasinpress run` feed-to-publish flow
- live Eitaa publishing after credential replacement
- production AI provider execution
- long-running scheduler/worker behavior
- production deployment configuration

## Configuration / secrets

The AI configuration supports an OpenAI-compatible provider and reads the API key through an environment-variable name. The repository also contains Eitaa publishing code, but credentials must remain external to source control.

The `.env` file was not present during the clean runtime inspection. The feed URL was available in the shell environment. This is important when diagnosing why a local run behaves differently from CI or a previously configured machine.

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
                    │             │
                    │       → AI (optional)
                    │             │
                    │       → Publish
                    │             │
                    └─────────────┘
```

The exact runtime relationship between YasinPress Rewrite and other Yasin content projects must remain evidence-based. In particular, it should not be assumed that YasinPress Rewrite is interchangeable with YasinFeed or YasinRelay merely because their domains overlap.

## Evidence policy

This record intentionally separates:

- **verified implementation** — supported by repository files or executed tests;
- **runtime verification** — supported by an actual local execution;
- **historical verification** — reported from an earlier successful test;
- **pending verification** — behavior that still needs a fresh live test.

This follows the core YASIN-DOCS rule that planned or historical behavior must not be presented as current implementation without evidence.

## Next verification target

The next YasinPress verification step is a controlled end-to-end run:

1. provide a fresh valid publishing credential;
2. confirm feed configuration is loaded by the application, not only by the shell;
3. run the pipeline once;
4. inspect processing/publishing logs and result state;
5. confirm the destination receives the generated article;
6. record the exact verified configuration and result in this document.

No credential value should ever be written into YASIN-DOCS or the YasinPress repository.
