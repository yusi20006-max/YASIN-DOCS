# OpenFeed — Project Architecture Record

## Evidence Level

**README-verified / source audit pending**

## Identity

Repository: `yusi20006-max/Openfeed`

## Purpose

OpenFeed is a Go server plus lightweight PWA for reading public Telegram channels. Its documented fetch path uses the public Telegram preview through Google Translate domain fronting and uTLS, then exposes normalized JSON through a local HTTP API to the browser PWA.

## Responsibilities

- Fetch supported public Telegram channel content.
- Parse and normalize channel content.
- Expose a local HTTP API.
- Serve a lightweight PWA.
- Support media download where media is embedded in the Telegram preview.
- Maintain browser-side favorites/offline cache.

## Explicit Boundaries

The project documentation defines OpenFeed as the stable core of its ecosystem role. AI processing, scheduling, publishing, queue management, dashboards, and plugins are explicitly described as downstream responsibilities rather than new OpenFeed features.

## Runtime / Technology

- Go 1.22+
- PWA using HTML/CSS/JavaScript without a frontend framework
- Local HTTP server

## Documented Structure

```text
cmd/server/              server entry point
internal/telemirror/     Telegram fetching/parsing engine
internal/provider/       provider selection layer
internal/parser/         internal → public API transformation
internal/model/          public JSON models
internal/api/            HTTP handlers
web/                     PWA
```

## Documented API Surface

- `/api/channel`
- `/api/status`
- `/api/download`

Exact request/response contracts require source audit.

## Limits

- Public channels only.
- Private chats/groups are outside the documented scope.
- Media download depends on media being embedded in the public preview.
- Documented current download limit: 200 MB.

## Ecosystem Relationship

OpenFeed is a related integration/data-ingestion component. FeedBridge documents that it vendors a fetcher derived from OpenFeed's `telemirror` engine and does not require a separate OpenFeed runtime instance. This establishes implementation lineage, but not necessarily a runtime dependency.

## Audit Remaining

- Full source tree verification
- Package/module dependency graph
- HTTP contracts
- Configuration and environment
- Error handling
- Tests and CI
- Security review
- Performance characteristics
- Release/versioning policy
- Exact relationship with YasinRelay and FeedBridge
