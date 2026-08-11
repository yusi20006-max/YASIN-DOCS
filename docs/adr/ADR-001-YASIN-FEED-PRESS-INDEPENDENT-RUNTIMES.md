# ADR-001 — YasinFeed and YasinPress Are Independent Application Runtimes

- Status: Accepted
- Date: 2026-08-10
- Scope: YasinFeed, YasinPress, YasinHub, YasinCLI

## Decision

YasinFeed and YasinPress are two separate, independently runnable application products.

Each project must be able to:

- install independently;
- configure its own runtime independently;
- start and stop independently;
- own its own application state;
- run its own content pipeline;
- publish through its own supported publishers;
- operate without importing the other project's internal modules.

Neither project is a required runtime dependency of the other.

## YasinFeed

YasinFeed remains the general-purpose content aggregation, processing, storage, rewriting, and publishing platform.

Its runtime pipeline and release lifecycle are owned by the YasinFeed repository.

## YasinPress

YasinPress remains the specialized Persian-news publishing application, primarily targeting Eitaa.

Its RSS ingestion, news classification, priority/breaking detection, formatting, queueing, and publishing pipeline are owned by the YasinPress repository.

## Relationship

The projects may share architectural ideas, provider conventions, or future reusable contracts, but conceptual overlap does not create a runtime dependency.

```text
                    YasinHub / YasinCLI
                     operational control
                       /           \
                      ▼             ▼
                 YasinFeed     YasinPress
                  standalone      standalone
                  runtime         runtime
```

Hub/CLI operational control is optional from the application's internal perspective: the applications must remain capable of executing their own core logic without importing Hub internals.

## Storage

YasinFeed and YasinPress retain separate application state. No shared database is implied by this decision.

## AI

Neither application is required to depend on Yasin-AI. Each may use its own provider abstraction until a future, explicitly approved integration contract is introduced.

## Consequences

### Positive

- Each application can be deployed and tested independently.
- A failure or release cycle in one application does not block the other.
- Project ownership and debugging boundaries remain clear.
- YasinPress can remain specialized without forcing YasinFeed to adopt news-specific behavior.
- YasinFeed can evolve as a general platform without becoming coupled to Press requirements.

### Trade-off

Some ingestion, processing, configuration, and publishing code may remain duplicated. Reuse should be introduced deliberately through shared libraries or contracts rather than by making one application depend on the other.

## Non-Goals

This ADR does not prohibit future shared libraries, APIs, provider gateways, or common content contracts. It only prohibits treating either application as a mandatory runtime dependency of the other without a new architectural decision.

## Validation Rule

Any future change that makes YasinFeed require YasinPress, or YasinPress require YasinFeed, must supersede this ADR with an explicit architecture decision and source-level implementation evidence.
