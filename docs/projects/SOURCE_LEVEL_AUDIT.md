# Yasin Ecosystem — Source-Level Architecture Audit

**Status:** Phase 5 deep audit — initial evidence pass  
**Verified:** 2026-08-09

This document records implementation-level evidence gathered from repository manifests and configuration files. It deliberately does not infer facts that were not directly observed.

## 1. Yasin-Core

### Packaging

`pyproject.toml` identifies the package as `yasin-core`, describes it as the kernel/runtime foundation, and declares Python `>=3.9`. Runtime dependencies include `requests`, `python-dotenv`, and `PyYAML`; `psutil` is optional for observability. The package discovery includes `yasin_core*` and `yasinrelay*`. fileciteturn66file0

### Architectural implication

The packaging metadata provides direct evidence that Yasin-Core is a Python distribution and that its packaging boundary currently includes a `yasinrelay*` namespace. This is important and requires further source inspection before deciding whether that namespace represents an intentional embedded subsystem, compatibility package, or historical boundary.

## 2. Yasin-AI

### Packaging

`pyproject.toml` identifies the distribution as `yasinai` version `1.0.0`, requires Python `>=3.8`, and has `cryptography>=42,<47` as its runtime dependency. Its optional test dependencies are `pytest` and `pytest-cov`. The executable entry point is `yasin = yasinai.cli.security_entrypoint:main`. Package discovery includes `yasinai*`, `security_platform*`, `developer_platform*`, `knowledge_platform*`, `api_service*`, and `observability*`. fileciteturn69file0

### Architectural implication

This strongly supports the earlier classification of Yasin-AI as a modular platform rather than a single provider adapter. Its package boundary explicitly contains security, developer, knowledge, API, and observability namespaces.

`requirements.txt` currently contains only the cryptography runtime requirement, confirming that the larger feature set is either implemented with the standard library/internal modules or managed through the package metadata and optional groups. fileciteturn68file0

## 3. YasinHub

`requirements.txt` declares `pytest`, `pyyaml`, and `rich`. fileciteturn74file0

This supports a Python implementation with testing, YAML/configuration handling, and terminal-oriented presentation. It does not by itself prove any runtime dependency on Yasin-Core or Yasin-Agent.

## 4. YasinRelay

`requirements.txt` declares `requests` and `python-dotenv`. fileciteturn70file0

This supports an HTTP/API-oriented Python component with environment-based configuration. The absence of a `pyproject.toml` in the queried default branch means packaging ownership should be documented separately after inspecting the actual repository tree.

## 5. YasinFeed

`requirements.txt` currently declares `PyYAML` and `feedparser`. fileciteturn71file0

This directly supports YAML configuration and RSS/feed ingestion as implementation concerns. It does not prove that AI execution or publishing is implemented through another Yasin repository.

## 6. YasinPress

`requirements.txt` declares HTTP/RSS parsing, HTML parsing, XML handling, date/time processing, Persian/Jalali date support, fuzzy matching, scheduling, and Persian text shaping dependencies. fileciteturn72file0

This gives stronger implementation-level evidence for the project's news-ingestion, normalization, duplicate detection, scheduling, and Persian-content processing responsibilities.

## 7. YasinCLI

`package.json` identifies YasinCLI as a CommonJS Node.js package, with `src/index.js` as its main entry point and `yasin.sh` as the executable command. It defines Jest tests, ESLint linting, and a Node smoke test. The repository URL is `yusi20006-max/Yasin-cli`, and the queried package metadata is on the `initial-setup` branch. fileciteturn73file0

### Architectural implication

YasinCLI is independently packaged and tested. Its manifest does not declare a Node dependency on Yasin-Core, YasinHub, or another Yasin package. Any integration should therefore be treated as runtime/process/API integration until source evidence proves otherwise.

## 8. FeedBridge

The README states that the Telegram fetcher is vendored into the repository and is built as part of the repository, rather than deployed as a separate OpenFeed service. It is invoked as `fetcher/fetch <channel_username>` and its JSON stdout is consumed by the Fetch Engine. fileciteturn51file0

### Architectural implication

The verified relationship is **lineage/reuse**, not a runtime dependency on a separate OpenFeed process.

## 9. TJC

TJC is a POSIX-shell CLI platform for Google Jules API workflows. Its README documents a YAML/JSON workflow engine, strict validation, scheduler support, plugins, reporting, and compatibility with Linux/Termux. fileciteturn52file0

### Architectural implication

TJC is best treated as developer automation infrastructure supporting the development lifecycle, not as a Yasin runtime component.

## 10. Termux Backup Manager

The README identifies Google Drive backup, restore, migration, backup management, Termux, `rclone`, and a Google Drive remote as its core scope. fileciteturn53file0

### Architectural implication

This is operational/support tooling rather than an application-layer Yasin service.

## 11. Evidence Summary

| Project | Implementation evidence obtained | Key result |
|---|---|---|
| Yasin-Core | `pyproject.toml` | Python foundation package; notable `yasinrelay*` package discovery |
| Yasin-AI | `pyproject.toml`, requirements | Modular Python AI platform with multiple package domains |
| YasinHub | requirements | Python/config/test/terminal tooling |
| YasinRelay | requirements | Python HTTP/env-oriented component |
| YasinFeed | requirements | YAML + RSS ingestion evidence |
| YasinPress | requirements | News/RSS/HTML/Persian/scheduling stack |
| YasinCLI | `package.json` | Node CLI with Jest/ESLint/smoke tests |
| FeedBridge | README/build instructions | Vendored fetcher; no separate OpenFeed runtime required |
| TJC | README/docs references | Workflow/scheduler/plugin developer automation |
| Termux Backup Manager | README | Termux/rclone/Google Drive operational tooling |

## 12. Still Required

The following cannot be considered complete from manifest evidence alone:

- complete source tree/module graph;
- import-level dependency graph;
- public API signatures;
- runtime entry-point call graph;
- actual persistence schemas;
- CI workflow contents and recent run status;
- issue/PR/release state;
- producer/consumer contracts;
- security-sensitive boundaries;
- deployment topology.

Those items remain in Phase 5 deep audit scope.
