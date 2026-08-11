# TJC Release Status

## Current Release

| Field | Value |
|---|---|
| Project | TJC (Termux Jules CLI) |
| Version | `v2.1.1` |
| Release status | **Stable / Released** |
| Release type | Maintenance / test-stability release |
| Release URL | https://github.com/yusi20006-max/TJC/releases/tag/v2.1.1 |
| Release commit | `16600ba6ec799f51a50c74cc79c7a64144ff1bda` |
| Test status | **11/11 test suites passing** |
| Pre-release | No |

## Final Validation Status

TJC v2.1.1 is the completed, test-stable release following the v2.1 stabilization and hardening cycle.

The final cycle resolved the remaining test failures and compatibility issues, including:

- Python-based `yq` compatibility by removing unsupported Go `yq` CLI options.
- YAML type assertions aligned with JSON types produced by Python-based `yq`.
- Plugin v2.1 test isolation and missing output/color helper dependencies.
- MCP Server JSON-RPC response construction and strict `jq --argjson` parsing.
- Audit test expectations for redacted values.
- Queue lock handling caused by POSIX shell dynamic variable scoping.
- Queue priority metadata and persistence validation.

## Test Evidence

The release baseline was verified with the complete TJC test suite:

- **11 test suites passed**
- Queue isolation test: **4/4 passed**
- No remaining `jq: invalid JSON text passed to --argjson` error in the isolated queue diagnostic.
- Release is published as a normal stable release, not a pre-release.

## Related Completion Work

The TJC stabilization/release hardening work was completed through the project's GitHub issues and pull requests. The final release commit is:

`16600ba6ec799f51a50c74cc79c7a64144ff1bda`

Relevant completed release/hardening issues included #42, #47, and #50.

## Architectural / Ecosystem Status

TJC is treated as the Termux-oriented Jules CLI component in the Yasin development tooling ecosystem. Its implementation remains in the TJC repository; this document records only the ecosystem-level release state.

For implementation details, source code, tests, and release artifacts, use the TJC repository as the source of truth.

## Next State

**TJC v2.1.1 is complete and released.** Future work should begin from this stable baseline rather than reopening the completed stabilization cycle unless a new regression or feature requirement is identified.
