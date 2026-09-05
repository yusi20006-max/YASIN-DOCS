# Yasin Startup Registry

This registry is the canonical, secret-free startup reference. It records repository identity, responsibility, and operational entrypoint location without storing credentials.

| Project | Responsibility | Startup/control reference |
|---|---|---|
| YasinHub | Control Plane / lifecycle / PID authority | `docs/operations/STARTUP_RUNBOOK.md` + project README |
| Yasin-Agent | Agent/workflow runtime | Project README + Hub lifecycle control |
| YasinRelay | Content relay/publish pipeline | Project README + Hub lifecycle control |
| Yasin-AI | Canonical AI capability plane | Project README + Hub lifecycle control |
| Yasin-MCP | MCP protocol/tool boundary | Project README |
| Yasin-Operations | Optional operations provider/gateway | Project README |

## Rules

- Do not store API keys, tokens, passwords or private channel identifiers in this registry.
- Use each project's documented configuration procedure for secrets.
- Use YasinHub for ecosystem lifecycle operations.
- Verify actual process/PID state after lifecycle operations.
- Update this registry when a canonical entrypoint or ownership boundary changes.

## Current acceptance baseline

See `FINAL_ECOSYSTEM_ACCEPTANCE_ISSUE_174.md` for the current evidence and remaining blockers.
