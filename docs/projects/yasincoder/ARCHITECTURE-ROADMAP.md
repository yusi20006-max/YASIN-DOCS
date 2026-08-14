# YasinCoder — Architecture & Production Roadmap

Status: **Phase 2 in progress**  
Audit date: **2026-08-14**  
Repository: [`yusi20006-max/YasinCoder`](https://github.com/yusi20006-max/YasinCoder)  
Default branch: `master`

## 1. Canonical role

YasinCoder is the canonical repository for the Yasin coding-agent application. The implementation, local AI gateway, provider orchestration and coding workflows should converge here rather than being split across multiple coding-agent repositories.

This does **not** make YasinCoder the owner of the entire Yasin ecosystem. It owns the coding-agent boundary and consumes shared ecosystem capabilities through explicit contracts.

## 2. Target architecture

```text
                         YasinCoder
                              │
             ┌────────────────┼────────────────┐
             │                │                │
        Agent Core       Project Brain      Commands
             │                │                │
             └────────────────┼────────────────┘
                              │
                        AI Provider Layer
                              │
                ┌─────────────┴─────────────┐
                │                           │
          Local AI Gateway             Cloud Providers
                │                           │
          ┌─────┴─────┐              Gemini / other
          │           │
       Qwen local   Gemini CLI
       llama.cpp
          │
     127.0.0.1:18080
          ▲
          │
   Web Control/UI
   127.0.0.1:18765
```

## 3. Verified current runtime

| Component | Verified state |
|---|---|
| Python gateway | running |
| Web port | `127.0.0.1:18765`, HTTP 200 |
| Qwen server | healthy on `127.0.0.1:18080` |
| Model | Qwen3 1.7B Q4_K_M |
| Alias | `qwen3-local` |
| Context | configured 4096 |
| Gemini CLI | installed and discoverable |
| ripgrep | Termux 15.2.0 installed |
| Qwen generation | verified through `/api/qwen` with `QWEN_OK` |
| Gemini generation | blocked at audit time by daily quota 429 |

## 4. Gateway contract

The local gateway is the control plane between the browser and provider runtimes.

### Read

- `/api/status`
- `/api/logs`

### Lifecycle

- `/api/start`
- `/api/stop`
- `/api/restart`

### Provider calls

- `/api/qwen`
- `/api/gemini`

The UI should depend on these stable contracts rather than on llama.cpp or Gemini CLI implementation details.

## 5. Qwen local boundary

Qwen runs as a separate `llama-server` process. This keeps the model runtime replaceable and lets the Python gateway remain focused on orchestration.

Observed model metadata includes approximately 2.03B parameters, 1.276 GB GGUF size, Q4_K Medium quantization, four slots and a configured 4096-token context.

## 6. Gemini boundary

Gemini is an external CLI provider. The gateway can discover and invoke the CLI. During the 2026-08-14 audit, the CLI returned `TerminalQuotaError` / HTTP 429 because the configured `gemini-3.5-flash` quota was exhausted.

Evidence classification:

- CLI installed: **Confirmed**
- Gateway route exists: **Confirmed**
- Successful Gemini generation during this audit: **Not verified**
- Quota failure: **Confirmed**

## 7. Security boundary

The Qwen server is localhost-only, but llama.cpp reports CORS `*` and no API key. This is acceptable only for the current local development setup.

Before remote exposure, YasinCoder must add authentication, restrictive CORS, rate limiting, command approval/allowlisting, secret isolation and process/PID hardening.

## 8. Known issues

1. Duplicate `/api/start` and `/api/stop` route branches were visible during route inspection.
2. Gemini CLI continued to print a ripgrep-unavailable fallback after `rg` 15.2.0 was installed; investigate environment/path propagation.
3. Provider quota errors need a first-class normalized state.
4. Larger local models require device-specific RAM/latency benchmarks before adoption.

## 9. Roadmap

### Phase 0 — Ownership and baseline — COMPLETE
- Canonical YasinCoder repository established.
- Modular coding-agent structure retained.

### Phase 1 — Local runtime — COMPLETE
- Gateway, Qwen runtime, UI, lifecycle scripts and control routes verified.

### Phase 2 — Provider integration — IN PROGRESS
- Normalize provider contracts.
- Add health states.
- Add quota-aware fallback.
- Fix Gemini environment detection.
- Add timeout/cancellation and structured telemetry.

### Phase 3 — Coding execution core — NEXT
- Provider interface.
- Safe filesystem tools.
- Patch/diff operations.
- Command execution policy.
- Test runner.
- Git operations.
- Session/checkpoint model.

### Phase 4 — Project intelligence
- File/symbol/import indexes.
- Dependency graph.
- Semantic search.
- Project memory.
- Change-impact analysis.

### Phase 5 — Agent workflows
- Plan/edit/test loop.
- Fix/review/refactor/explain workflows.
- Bounded autonomous execution.
- Approval gates and rollback.

### Phase 6 — Local AI maturity
- Benchmark current Qwen.
- Evaluate larger local models.
- Model registry and dynamic context.
- Streaming and runtime capability detection.

### Phase 7 — Cloud/fallback orchestration
- Gemini and additional OpenAI-compatible providers.
- Priority chain, retries, circuit breaker and quota-aware routing.

### Phase 8 — Web control plane
- Provider dashboard, model selector, chat, task execution, diff/test approval and filtered logs.

### Phase 9 — Security/reliability
- Authentication, CORS, rate limiting, secret redaction, crash recovery, liveness/readiness and regression tests.

### Phase 10 — Production packaging
- Termux/Linux installer, one-command operations, model helper, backup/restore, CI and releases.

## 10. Definition of done

YasinCoder reaches production maturity when it can safely inspect a project, select a provider, execute bounded coding changes, run tests, present a diff, recover from provider/process failure, operate with a local model when configured, and protect secrets/destructive operations.
