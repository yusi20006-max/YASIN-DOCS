# Operations Documentation

Cross-project operational knowledge is maintained here.

## Canonical operational entry point

- **[Yasin Ecosystem Startup Runbook](../STARTUP_RUNBOOK.md)** — canonical startup, lifecycle, configuration, security, publish-acceptance, and handoff procedure.
- **[Real Publish Acceptance — 2026-09-06](REAL_PUBLISH_ACCEPTANCE_2026-09-06.md)** — recorded PASS for the real-publish gate, including the non-secret Eitaa receipt evidence and the remaining PWA visual gate.
- **[Termux Canonical Project Layout](TERMUX_CANONICAL_PROJECT_LAYOUT.md)** — mandatory local filesystem convention.

The startup runbook is the first operational document to read for a new operator or AI coding session. It points to `Yasin-Operations` for persisted runtime evidence instead of relying on chat history.

## Scope

Operational topics include:

- service lifecycle;
- health and diagnostics;
- configuration;
- deployment;
- observability;
- backup and recovery;
- incident and troubleshooting procedures;
- real publish acceptance and evidence handling.

Operational details that belong exclusively to a single project should remain in that project's repository and be referenced here when necessary.

## Evidence rule

Operational documents must distinguish implementation intent from runtime evidence. Do not record PASS/COMPLETED without command output, test output, API response, process/PID evidence, or browser evidence appropriate to the claim. Never store secrets, tokens, credentials, or `.env` contents.
