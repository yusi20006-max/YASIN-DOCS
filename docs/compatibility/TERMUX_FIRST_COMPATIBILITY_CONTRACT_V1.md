# Termux-First Compatibility Contract v1

**Status:** Target / ecosystem-wide architectural requirement  
**Scope:** All Yasin Ecosystem repositories intended to operate together on Termux/Android  
**Owner:** YASIN-DOCS  
**Effective:** 2026-09-04

## 1. Purpose

Yasin Ecosystem is **Termux-first** for its supported mobile development and runtime environment.

Termux/Android compatibility is not treated as an after-the-fact portability check. Projects that participate in the Yasin runtime must be designed, packaged, tested, and documented so that the canonical Termux environment is a first-class target.

This contract exists to prevent cross-project failures caused by Python-version assumptions, native dependencies, Android ABI differences, Linux desktop service assumptions, filesystem differences, and incompatible runtime entrypoints.

## 2. Canonical Termux Target

The current reference environment is:

| Property | Canonical target |
|---|---|
| OS | Android via Termux |
| Architecture | ARM64 / aarch64 |
| Android | Android 11 / API level 30 reference device |
| Python | Python 3.14.x reference runtime |
| Project root | `$HOME/yasineco/<REPO>` |
| Process model | Android/Termux processes; no mandatory systemd dependency |
| Native builds | Must be validated on the actual Termux target when required |

The exact device and package versions may evolve, but the compatibility principle remains: **new Yasin code must not silently assume a conventional desktop Linux environment when an Android/Termux equivalent is required.**

## 3. Mandatory Compatibility Rules

### 3.1 Python

Every Python project must explicitly document:

- supported Python versions;
- the reference Python version used in Termux validation;
- dependencies known to have native extensions;
- known Python-version limitations;
- reproducible installation commands for Termux.

A broad declaration such as `requires-python = ">=3.9"` is not sufficient evidence of compatibility with Python 3.14 on Android.

Python compatibility must be established by installation and import/runtime tests, not metadata alone.

### 3.2 Native dependencies

Dependencies containing Rust, C, C++, OpenSSL, cffi, or other native components require explicit Termux validation.

A package being installable is not sufficient. The resulting native extension must also successfully load at runtime.

For example, a successful build of a wheel followed by an Android dynamic-linker error is classified as **not compatible** until resolved.

### 3.3 Android ABI

For native Python extensions and other compiled components, validation must cover:

- Android API level;
- ARM64/aarch64 architecture;
- the actual Termux Python runtime;
- dynamic loading/import of the compiled artifact.

Build-only success must never be recorded as runtime compatibility.

### 3.4 Rust / maturin

Rust-backed Python dependencies must document their Android build requirements when applicable, including environment variables such as `ANDROID_API_LEVEL` when required by the build system.

A dependency must be tested after installation with its real import path. Build metadata generation alone is insufficient.

### 3.5 Filesystem

All ecosystem repositories used together on Termux MUST live under:

```text
$HOME/yasineco/<REPO>
```

Legacy paths such as `$HOME/yasin-ecosystem/` and `-main` directory variants are non-canonical and must not be introduced into active runtime configuration.

### 3.6 Process and service lifecycle

Services must not require systemd, desktop init systems, or other non-Termux infrastructure unless an explicit adapter exists.

Every managed service must have a documented Termux-compatible:

- start command;
- stop mechanism;
- restart mechanism;
- process/PID verification method;
- health/readiness check where applicable;
- foreground/debug invocation.

YasinHub service controls must operate on real processes. Simulated lifecycle state does not satisfy this contract.

### 3.7 CLI entrypoints

Every service intended to be managed by YasinHub must have a deterministic non-interactive startup path.

Interactive configuration prompts, TTY requirements, desktop-only launchers, or shell-specific assumptions must not be part of an automated service startup path.

### 3.8 Go and other compiled components

Go binaries used by Yasin projects must be buildable and executable on the canonical ARM64 Termux environment, or the project must provide a documented compatible artifact/alternative.

The binary itself must be executed in a real smoke test; successful compilation alone is insufficient.

## 4. Evidence States

Compatibility findings use the YASIN-DOCS evidence model:

- **Confirmed** — installation and runtime behavior verified on the canonical Termux target.
- **Target** — required compatibility behavior that the project must satisfy but is not yet fully verified.
- **Proposed** — possible future implementation option.
- **Unresolved** — investigation is required before compatibility can be claimed.

Never mark a project Termux-compatible solely because its package metadata permits the target Python version.

## 5. Required Validation Levels

Each project should be classified against these levels:

### Level 0 — Metadata

Package metadata declares a compatible Python/platform range.

**Not sufficient for Termux compatibility.**

### Level 1 — Installation

Dependencies install successfully in the canonical Termux environment.

### Level 2 — Import / Load

The installed Python packages and native extensions import/load successfully.

### Level 3 — Runtime Smoke Test

The actual application entrypoint executes on Termux and performs its basic function.

### Level 4 — Integration

The application communicates correctly with its Yasin ecosystem dependencies on Termux.

### Level 5 — Operational

YasinHub or the appropriate control surface can start, stop, restart, and verify the real process, and health/readiness behavior is confirmed where applicable.

A project should be called **Termux-first compatible** only after the level appropriate to its role has been demonstrated, with application/service projects targeting Levels 3–5.

## 6. Ecosystem Compatibility Matrix

This matrix is a living record. Entries must be based on evidence rather than assumptions.

| Project | Python 3.14 | Android ARM64 | Native deps | Runtime | Integration | Operational | Current state |
|---|---:|---:|---:|---:|---:|---:|---|
| YasinHub | Confirmed | Confirmed | Low | Confirmed | Confirmed | Confirmed | **Confirmed** |
| Yasin-Agent | Confirmed | Confirmed | FastAPI/Pydantic native components validated | Confirmed | Confirmed | Confirmed | **Confirmed** |
| YasinRelay | Confirmed | Confirmed | Go + Yasin-AI dependency chain | Confirmed without canonical Yasin-AI | Unresolved | Target | **Unresolved** |
| Yasin-AI | Confirmed installation path | Unresolved | cryptography/Rust | Unresolved | Target | Target | **Unresolved** |
| YasinPress | Confirmed runtime | Confirmed runtime | Development tooling has native build considerations | Confirmed | Target | Target | **Target / partial evidence** |
| Yasin-Core | To verify | To verify | To verify | To verify | To verify | N/A | **Unresolved** |
| YasinCLI | To verify | To verify | To verify | To verify | To verify | To verify | **Unresolved** |

This matrix must be updated whenever new compatibility evidence is produced.

## 7. Current Known Case: Yasin-AI + YasinRelay

The first implementation audit under this contract identified a concrete issue:

```text
YasinRelay
    -> Yasin-AI 1.1.4
        -> cryptography >= 48.0.1
            -> cryptography 50.0.1
                -> Rust native extension
                    -> Android dynamic loading
```

On the reference Termux environment, `cryptography 50.0.1` successfully built and installed after setting `ANDROID_API_LEVEL=30`, but importing its Rust extension failed with:

```text
ImportError: dlopen failed: cannot locate symbol "PyModule_Type"
```

Therefore:

- installation success is **Confirmed**;
- runtime compatibility of this dependency chain is **Unresolved**;
- Yasin-AI integration in YasinRelay must not be declared complete until the import/runtime issue is resolved and a real Relay generation test passes.

This example establishes the required standard for future investigations: **build success is not runtime compatibility.**

## 8. Project Requirements

Every ecosystem project should maintain a project-level compatibility section or runbook containing:

1. supported Python versions;
2. canonical Termux install command;
3. required Android/API assumptions;
4. native dependency notes;
5. environment variables required for Android builds;
6. runtime smoke-test commands;
7. service lifecycle commands where applicable;
8. known incompatibilities;
9. evidence date and validation environment.

Cross-project compatibility requirements belong here; implementation details remain in the project repositories.

## 9. Change Governance

Changes that affect the ecosystem-wide Termux contract must update this document and, when appropriate:

- the canonical dependency matrix;
- the affected project's architecture/runbook;
- an ADR for an intentional cross-project architectural decision;
- CI or smoke-test configuration.

Dependency version changes that are made solely to work around Android compatibility must be documented with the affected versions, observed failure, selected version, and runtime evidence.

## 10. Definition of Done

A Termux-first compatibility task is complete only when:

- installation succeeds on the reference environment;
- native extensions, if any, load successfully;
- the actual entrypoint runs;
- required integration calls work;
- service lifecycle is real and verifiable where applicable;
- tests/smoke tests pass;
- the compatibility matrix reflects the evidence;
- no unsupported assumption is hidden behind a generic Python/platform declaration.

**Principle:**

> Termux is a first-class Yasin runtime target. Compatibility must be proven at runtime, not inferred from package metadata or successful compilation.
