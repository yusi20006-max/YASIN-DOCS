# YasinFeed — Publisher & Runtime Audit v1

- Repository: `yusi20006-max/Yasinfeed`
- Audit date: 2026-08-12
- Scope: Publisher layer, runtime lifecycle, configuration boundary, independent publishing readiness
- Status: **Core runtime verified; publisher layer has an important implementation gap**

## 1. Runtime lifecycle

`yasinfeed.main` creates `YasinFeedEngine`, registers OS shutdown handlers, initializes the engine, then starts it. The engine owns configuration loading, logging setup, module registration, initialization order, startup order, shutdown order, and the blocking runtime loop.

The registration order is:

```text
Monitoring
Integration
Storage
Models
Auth
Rewrite
Fetch
Publisher
Scheduler
API
```

The engine therefore provides a genuine standalone application lifecycle and does not require YasinHub or Yasin-Agent to boot.

## 2. Configuration boundary

The default publisher configuration currently disables all three output channels:

```yaml
publisher:
  eitaa:
    enabled: false
  pwa:
    enabled: false
  rss:
    enabled: false
```

The configuration loader supports environment overrides through `YASINFEED_` variables and nested `__` paths. This means publishing can be enabled without changing the core source tree.

The loader also masks sensitive values when configuration is exposed through diagnostic paths and applies restrictive file permissions where possible.

## 3. Publisher module — current implementation

`PublisherModule` recognizes three channels:

```text
Eitaa
PWA
RSS
```

Eitaa has a concrete publisher object and an actual HTTP send path.

PWA and RSS currently have only placeholder methods. Their current behavior is effectively:

```text
publish_to_pwa(data) → log → True
publish_to_rss(data) → log → True
```

when enabled.

This is the main finding of this audit: **the README describes PWA and RSS as publishing outputs, but the current PublisherModule does not yet generate or persist those outputs.**

## 4. Eitaa publishing

The Eitaa publisher is a concrete HTTP adapter. It constructs:

```text
https://eitaayar.ir/api/{TOKEN}/sendMessage
```

and submits `chat_id` and `text` using a standard-library HTTP request.

Therefore Eitaa is not a stub at the publisher level.

The implementation catches all exceptions and returns `None`, while the module translates a non-empty response into a successful publish result.

Operationally, this should later be tightened to distinguish:

- transport failure;
- HTTP failure;
- malformed response;
- successful Eitaa response.

## 5. Scheduler → Publisher boundary

The architecture documentation describes a default `fetch_and_process` automation cycle which ultimately publishes to Eitaa/RSS/PWA. The engine itself starts the Scheduler and Publisher as independent modules.

The important verification requirement for the next runtime test is therefore not simply `python -m yasinfeed.main` booting. We need to prove the actual data path:

```text
Feed source
  ↓
FetchModule
  ↓
Article/model creation
  ↓
Storage
  ↓
Rewrite
  ↓
Publisher
  ↓
actual destination
```

A successful engine boot alone does not prove this end-to-end path.

## 6. Independent-operation result

The current source structure supports independent YasinFeed execution:

```text
YasinFeed
├── config
├── fetch
├── rewrite
├── storage
├── publisher
├── scheduler
├── api
└── engine
```

YasinHub and Yasin-Agent are not required imports for the engine lifecycle.

The IntegrationModule is an extension boundary, not a boot-time orchestration dependency.

This preserves the agreed ecosystem rule that YasinFeed and Yasin-Agent/YasinHub remain separately runnable products.

## 7. Publisher maturity matrix

| Channel | Current state | Assessment |
|---|---|---|
| Eitaa | Real HTTP adapter | Functional path exists |
| PWA | Placeholder publisher method | Needs real output implementation |
| RSS | Placeholder publisher method | Needs real XML generation/output implementation |
| Scheduler integration | Architecture says supported | Requires live end-to-end verification |
| Standalone engine | Implemented | Functional lifecycle |

## 8. Required next work

Before treating YasinFeed publishing as completely production-ready, the next implementation/audit pass should:

1. Run the scheduler with a real RSS source.
2. Verify an item becomes an Article.
3. Verify storage persistence.
4. Verify rewrite behavior with the default provider.
5. Verify Eitaa publishing independently.
6. Implement and verify real RSS output.
7. Implement and verify real PWA JSON output.
8. Verify API exposure of produced content.
9. Repeat the complete flow on Termux.

## 9. Architectural conclusion

**Do not move publishing responsibilities into YasinHub or Yasin-Agent.**

YasinFeed should remain responsible for the actual transformation and delivery adapters. Hub/Agent may orchestrate or consume the service through integration interfaces, but YasinFeed must remain capable of operating alone.

The current code already satisfies the independence boundary. The remaining issue is implementation completeness of the PWA/RSS publishers and live verification of the complete scheduler pipeline.
