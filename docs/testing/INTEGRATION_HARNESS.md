# Cross-repository mock integration harness

**Issue:** YASIN-DOCS #11

## Goal

Contract-level integration tests between Yasin-AI public APIs and consumer adapter patterns **without** live/paid providers.

## Coverage

- Request contract (`GenerationRequest` fields preserved)
- Response contract (success text)
- Error contract (exception → consumer semantics)
- Provider fallback (empty text)
- Model/provider preservation on the request object

## Consumer failure semantics (encoded)

| Consumer | On AI failure |
|----------|----------------|
| Relay | Passthrough original text |
| Feed | Raise |
| Press | Structured `PressAIResult(ok=False)` |

## Usage

```bash
pytest tools/integration_harness/tests/ -q
```

Offline only. Live external providers require a separate issue.
