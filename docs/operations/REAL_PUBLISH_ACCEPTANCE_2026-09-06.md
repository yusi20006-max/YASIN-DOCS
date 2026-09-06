# Real Publish Acceptance — 2026-09-06

**Status:** PASS for the real-publish gate
**Acceptance anchor:** YasinHub Issue #174
**Runtime:** Android 11 / Termux / ARM64 / Python 3.14.6
**Evidence source:** `yusi20006-max/Yasin-Operations/reports/active/real-publish-acceptance.md`

## Result

The previously operator-blocked real-publish gate was executed after valid runtime configuration was provisioned locally. The canonical lifecycle/control path was used, and the resulting Eitaa publish response was recorded as runtime evidence.

Verified facts recorded by the Operations audit:

- source processing used `@bbcpersian`;
- the configured Eitaa destination was `@yasinrelay`;
- the publish request was accepted by Eitaa;
- receipt: `success=True`;
- receipt `message_id=169818801`;
- Relay tests: 108 passed;
- Hub tests: 478 passed;
- no token, API key, or other credential value is recorded here.

## Boundary

This document records the **real-publish acceptance gate only**. It does not claim PWA visual acceptance. PWA visual acceptance still requires a real browser/mobile viewport and is intentionally deferred to the later Claude/UI pass.

## Operational rule

Do not repeat the publish operation merely to reproduce this evidence. Rerun it only when a new regression, configuration change, release, or acceptance cycle requires fresh runtime evidence.

## Canonical runbook

The canonical startup and operational procedure is:

`YASIN-DOCS/docs/STARTUP_RUNBOOK.md`

Operators and AI coding agents should start from that runbook, then consult the Operations evidence for the latest runtime acceptance record.

## Security

Secrets remain local runtime configuration. This document intentionally records variable names/results and non-secret receipt metadata only; it must never contain credentials or `.env` contents.
