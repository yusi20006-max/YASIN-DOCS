# Yasin-MCP Native Termux Compatibility Evidence

## Status

**CONFIRMED** for the tested native Termux environment.

This document records evidence from real execution of `Yasin-MCP` on Android/Termux. It does not claim universal Android compatibility across all Android versions, architectures, or Termux package states.

## Verified Environment

- OS: Android 13 kernel / Termux userspace
- Architecture: aarch64
- Python: 3.14.6
- `cryptography`: 50.0.1
- MCP: installed and importable
- Repository: `yusi20006-max/Yasin-MCP`

## Validation

The repository's Termux test runner completed successfully:

```text
Termux compatibility: OK
Python: 3.14.6
cryptography: 50.0.1
mcp: installed
402 passed, 2 skipped in 68.54s
```

The test suite was executed inside the native Termux virtual environment.

## Important Termux Runtime Boundary

Native Termux does not reliably execute temporary executable files containing a Python shebang directly. A file can exist and have executable permissions while direct `subprocess.run([path])` still fails with `FileNotFoundError`.

The verified solution is to execute Python gateway scripts through the active interpreter (`sys.executable`). A direct subprocess probe using the active Python interpreter and a `gateway` argument succeeded on the tested environment.

Yasin-MCP therefore treats Python gateway scripts as Python programs and launches them through the active Python interpreter when appropriate, rather than depending on direct shebang execution.

## Cryptography Boundary

An earlier native Termux/Python 3.14 environment exposed an ABI loading failure from the `cryptography` Rust extension (`PyLong_Type`). This was treated as a dependency/runtime compatibility issue rather than bypassed with an unsafe cryptographic fallback.

The currently tested environment has `cryptography 50.0.1` installed successfully and the complete test suite passes. The repository's dependency constraints and test runner should remain the source of truth for the exact supported dependency set.

## Evidence Classification

| Area | Result |
|---|---|
| Native Termux Python runtime | **CONFIRMED** (tested environment) |
| Python 3.14.6 | **CONFIRMED** |
| MCP import/install | **CONFIRMED** |
| Full repository test suite | **CONFIRMED** — 402 passed, 2 skipped |
| Operations Python gateway subprocess path | **CONFIRMED** |
| Universal Android compatibility | **NOT CLAIMED** |

## Related Repository Evidence

The Yasin-MCP compatibility work includes a Termux-specific test runner and Operations adapter handling for Python gateway scripts. These implementation details remain in `Yasin-MCP`; this document records the ecosystem-level compatibility evidence only.

## Governance

This record follows the YASIN-DOCS evidence policy: confirmed status is limited to behavior directly demonstrated by repository tests and real environment execution. Future Android/Termux environments should be revalidated if their Python, Termux packages, architecture, or cryptography build differs materially.
