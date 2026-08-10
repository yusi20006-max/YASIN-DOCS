# YasinCLI — Project Knowledge Pack

## Identity
- Intended repository: `YasinCLI`.
- Current GitHub repository lookup did not resolve a repository by the exact name during this documentation pass; therefore implementation details must not be stated as verified until the repository is located.
- Role established by ecosystem architecture: unified user-facing CLI and ecosystem orchestration layer.

## Owns
- Unified command UX
- Ecosystem-level orchestration
- Adapters to project public APIs/SDKs/process contracts
- Cross-project command composition

## Does Not Own
- Core runtime internals
- Agent execution internals
- Hub business logic
- Relay/Feed/Press content pipelines
- AI platform internals

## Canonical Position
```text
User
 ↓
YasinCLI
 ↓
Public SDK / API / Adapter
 ↓
YasinHub / Project runtime
```

YasinCLI should not become a competing implementation of YasinHub's control logic.

## Current Audit Knowledge
The architecture audit identified first-class adapter coverage for Core, Agent, Hub, and Relay. Feed, Press, and AI were identified as future explicit adapter work rather than assumed integrations.

## Change Rules
Every new cross-project command should delegate to the owning project's public boundary. Do not duplicate business logic in the CLI. Changes to adapter contracts should update the dependency matrix and API/compatibility documentation.

## Verification Status
**PARTIAL / NEEDS REPOSITORY RECONFIRMATION.** This card deliberately separates established ecosystem role from unverified repository implementation details.

## AI Agent Brief
Treat YasinCLI as the front door to the ecosystem. Before implementing a command, determine which project owns the underlying operation, then call that boundary through a stable adapter/API instead of reimplementing it.
