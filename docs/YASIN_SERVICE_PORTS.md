# Yasin Dedicated HTTP Service Port Contract

**Contract:** YasinHub Issue #179
**Status:** Canonical architecture contract
**Scope:** HTTP services in the Yasin ecosystem
**Canonical runtime root:** `~/YasinEco`

## 1. Reserved range

Yasin canonical HTTP services use the reserved range:

```text
7000–7099
```

Ports outside this range require an explicit, documented architecture exception.

## 2. Canonical allocation

Only runtimes with a verified HTTP listener receive a canonical HTTP port.

| Service | Port | Host | Health endpoint |
|---|---:|---|---|
| YasinHub | 7000 | `0.0.0.0`* | `/api/health` |
| Yasin-Agent | 7002 | `127.0.0.1` | `/v1/health` |
| YasinFeed | 7004 | `127.0.0.1` | `/api/health` |

`*` YasinHub is the documented binding exception because the PWA/dashboard must remain reachable through the Hub server. Lifecycle health checks still target `127.0.0.1`.

The canonical allocation is maintained in YasinHub's `yasinhub/ports.py`. The service registry consumes that allocation for lifecycle configuration.

## 3. Portless services

Services without a verified HTTP runtime are portless. They are not assigned synthetic ports merely for lifecycle management:

```text
YasinRelay       -> portless worker
                 launcher: .venv/bin/yasinrelay-termux run --schedule --non-interactive
                 process_pattern: yasinrelay.cli

Yasin-AI         -> portless worker/supervisor until an actual HTTP listener is verified
YasinPress       -> portless worker/CLI runtime
Yasin-Coder      -> portless/retired CLI entry (disabled in Hub registry)
eitaa_news_v2    -> retired worker
backup_manager   -> retired worker
```

A future HTTP runtime for any of these services may receive the next available
port only after its actual start command, bind behavior, process identity and
health endpoint are verified and registered centrally.

## 4. Process Identity and Port Ownership

For HTTP services, YasinHub verifies:

```text
Process Identity + Port Ownership + Health
```

For portless workers, YasinHub verifies:

```text
Process Identity + Liveness
```

A PID by itself never proves service identity.

## 5. Unknown-owner rule

```text
UNKNOWN PORT OWNER -> FAIL CLOSED
```

If an expected HTTP port is occupied by an unrelated process, YasinHub must not
kill it, terminate it, reuse its PID, or report the managed service as RUNNING.

## 6. Start contract

HTTP service:

```text
Process alive
AND identity matches
AND expected port owned
AND health succeeds
```

Portless worker:

```text
Process alive
AND identity matches
```

Process creation alone is insufficient.

## 7. Stop and restart contract

Restart verifies the old PID, stops only an identity-matching managed process,
verifies PID death and port release where applicable, then starts and verifies
the new process. The old PID is never proof of the new runtime.

## 8. Wrong-port rule

A service with a verified HTTP runtime that listens on a non-canonical port is
not RUNNING under the HTTP contract. A service classified as portless has no
expected HTTP port and therefore cannot fail merely because no port is open.

## 9. Host binding

Local HTTP services should bind to `127.0.0.1` unless external reachability is
explicitly required. YasinHub's `0.0.0.0` binding is the documented PWA exception.

## 10. Single Control Plane

YasinHub remains the sole Control Plane, lifecycle authority, and PID authority.

```text
PWA -> YasinHub
CLI -> YasinHub
```

The PWA never directly manages processes or ports.

## 11. Registry and compatibility

The executable registry is the lifecycle source of truth. It exposes, where
applicable:

```text
service_name
canonical_path
start_command
process_pattern
host
port
health_endpoint
```

The canonical runtime root is `~/YasinEco`. Stale local configuration must not
resurrect a retired or synthetic HTTP port assignment; canonical port metadata
comes from YasinHub's central allocation.

## 12. Migration rule

Legacy bindings such as `8000`/`8080`/`8101` are not canonical allocations after
Issue #179. Transitional overrides may remain where already supported, but new
canonical configuration must use only verified HTTP allocations.

## 13. Security rules

- Never log tokens or API keys.
- Never expose `.env` contents.
- Never kill an unknown port owner.
- Probe only expected service ports.
- Keep lifecycle authority in YasinHub.
- Fail closed when identity or ownership cannot be established safely.

## 14. Evidence and testing

Issue #179 requires automated coverage for allocation, reserved-range rules,
portless behavior, collision safety, Process Identity, Port Ownership, health,
PID death, port release, restart/new-PID behavior and wrong-port rejection.

Runtime claims require runtime evidence; source inspection alone is not runtime
proof.

## 15. Authority

This document is the YASIN-DOCS cross-repository statement of the Issue #179
contract. Executable allocation and lifecycle enforcement remain implemented by
YasinHub.
