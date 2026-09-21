# API Token Manager PWA — v1.0.0 Project Record

## Identity

- Repository: `yusi20006-max/api-token-manager-pwa`
- Release: `v1.0.0`
- Final commit: `a00e8fcbe4f6345ee762173086b4d67110080cdd`
- Runtime target: static PWA, with native Termux/Android ARM64 local acceptance
- System documentation: YASIN-DOCS
- Operational runbook: Yasin-Operations `docs/OPERATIONS-RUNBOOK.md`

## Scope

API Token Manager PWA is a local-first PWA for API configuration, provider detection, health checks, model discovery, capability evidence, diagnostics, safe local storage, and controlled export.

The project is a static PWA. It has no dedicated bundler/build server or application backend.

## Verified execution methods

### Local PWA on Termux

`bash
cd ~/api-token-manager-pwa
python -m http.server 8090
`

Open:

`text
http://127.0.0.1:8090/
`

The Python server is only a static file server.

### Node regression

`bash
cd ~/api-token-manager-pwa
npm test
`

Verified final result:

`text
60/60 tests passed
`

### Browser/PWA regression

The repository's authoritative browser suite runs in GitHub Actions with Ubuntu/Chromium:

`bash
npm install
npx playwright install chromium
npx playwright test
`

It covers PWA boot, delegated UI, reset/storage isolation, and Service Worker API-cache isolation. Real provider credentials are not required.

Native Termux/Android Playwright execution is not supported by the Playwright platform path used by the project. The install/test command fails with `Unsupported platform: android`. This is recorded as an environment limitation. Browser/PWA CI passed for the final commit.

### Hosted deployment

GitHub Pages is the hosted deployment path. The final deployment check passed.

## Initial problems and resolutions

### Browser test command

`npm run test:browser` does not exist in the current `package.json`. The correct browser command is the direct Playwright sequence used by CI:

`bash
npm install
npx playwright install chromium
npx playwright test
`

### npm ci

The repository does not track a `package-lock.json` in v1.0.0, so `npm ci` fails because its lockfile requirement is not satisfied. `npm install` is the correct dependency installation command for this release.

Generated `node_modules/` and `package-lock.json` were removed after local testing and were not committed.

### Native Android/Termux Playwright

`npx playwright install chromium` failed with:

`text
Unsupported platform: android
`

The same limitation prevents `npx playwright test` from running natively in Termux. GitHub Actions Browser/PWA CI was used as the authoritative browser regression environment.

### Local port collision

An initial local static server was started on port `8080` while OpenFeed traffic was also using that port. OpenFeed requests such as `/api/status`, `/api/channel/*` and `/api/image` reached the PWA static server and returned 404.

The collision was resolved by running API Token Manager PWA on port `8090`. The PWA then loaded successfully in the local browser.

## Major implementation and audit work

The final gap/regression audit was converted into independent issues and merged in sequence:

| Issue | Area | PR | Result |
| --- | --- | --- | --- |
| #35 | Service Worker / API cache isolation | #45 | Merged |
| #36 | CORS runtime contract | #46 | Merged |
| #37 | Google header authentication | #47 | Merged |
| #38 | Remove obsolete Phase 6 automation | #48 | Merged |
| #49 | Smart Setup alignment | #50 | Merged |
| #39 | Smart Setup auth evidence | #51 | Merged |
| #40 | Reset single invocation | #52 | Merged |
| #41 | Separate UI from storage | #53 | Merged |
| #42 | Browser/PWA regression suite | #54 | Merged |
| #43 | Provider/runtime documentation | #55 | Merged |
| #44 | OrcaRouter runtime smoke | #56 | Merged |

## Final runtime/security contracts

- Service Worker caches static same-origin assets only; provider API requests/responses are not cached.
- Google Gemini authentication uses `x-goog-api-key`; API keys are not put in Google request URLs.
- Browser-ambiguous fetch failures remain `NETWORK_ERROR` unless explicit evidence supports `CORS_BLOCKED`.
- Smart Setup separates discovery evidence from health evidence and reports `CONFLICTING_EVIDENCE` for contradictory evidence.
- Reset clears managed API/session state while preserving unrelated local storage.
- Capability Matrix treats `/models` as model-discovery evidence only; inference support requires separate evidence.
- OrcaRouter runtime smoke coverage verifies `/models`, `/chat/completions`, and `/responses` with mocked HTTP fixtures.
- Secrets are not included in console output, history, HealthResult, errors, DOM, URLs, default exports, or commits.

## Final acceptance evidence

`text
Main synchronized and clean
Node tests: 60/60 PASS
Browser/PWA CI: PASS
GitHub Pages: PASS
Local PWA on Termux: PASS
Native Termux Playwright: BLOCKED (Android unsupported)
Release v1.0.0: PASS
`

## Release

`text
v1.0.0
a00e8fcbe4f6345ee762173086b4d67110080cdd
`

This record is system-level documentation. Implementation details remain in the project repository, while operational commands belong in Yasin-Operations.
