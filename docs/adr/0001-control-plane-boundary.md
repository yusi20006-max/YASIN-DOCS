# ADR-0001: Keep Control Plane Separate From Application Pipelines

- **Status:** Accepted
- **Date:** 2026-08-11
- **Scope:** YasinCLI, YasinHub, Yasin-Core, Yasin-Agent, YasinFeed, YasinRelay, YasinPress

## Context

The ecosystem contains both control/management projects and content-processing applications. Combining those responsibilities would create unclear ownership and make application repositories responsible for ecosystem orchestration.

The canonical YASIN-DOCS architecture currently places YasinCLI as the user-facing control interface and YasinHub as the control/observability layer, while content applications remain responsible for their own collection, processing, and publishing pipelines.

## Decision

Yasin maintains a separation between:

- **Control plane:** YasinCLI and YasinHub;
- **Foundation/runtime:** Yasin-Core;
- **Agent/workflow execution:** Yasin-Agent;
- **Application pipelines:** YasinFeed, YasinRelay, YasinPress and related domain applications.

Application repositories must not silently become the ecosystem-wide service manager or control plane.

## Consequences

- Service lifecycle and ecosystem status can be centralized without coupling application logic to CLI implementation.
- Content applications can evolve independently.
- Cross-project orchestration belongs at the control-plane boundary.
- A request that changes this ownership model requires a new ADR or superseding ADR.

## Evidence

The current YASIN-DOCS README describes YasinCLI as the unified user interface, YasinHub as control + observability, and applications as the content-processing layer. The project registry also records YasinHub as a status/health aggregation layer and YasinFeed as owning collection, processing and publishing.

## Alternatives considered

### Put orchestration inside each application

Rejected. It duplicates lifecycle logic and blurs system boundaries.

### Make YasinHub own all application business logic

Rejected. YasinHub should coordinate and observe; domain applications should own domain processing.
