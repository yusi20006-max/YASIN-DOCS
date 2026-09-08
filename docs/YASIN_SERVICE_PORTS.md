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

Formally:

```text
7000 <= Yasin service port <= 7099
```

Ports outside this range require an explicit, documented architecture exception.

## 2. Canonical allocation

| Service | Port | Host | Health endpoint |
|---|---:|---|---|
| YasinHub | 7000 | `0.0.0.0`* | `/api/health` |
| Yasin-AI | 7001 | `127.0.0.1` | `/health` |
| Yasin-Agent | 7002 | `127.0.0.1` | `/v1/health` |
| YasinPress | 7003 | `127.0.0.1` | `/api/health` |
| YasinFeed | 7004 | `127.0.0.1` | `/api/health` |
| Yasin-Coder | 7005 | `127.0.0.1` | `/health` |

`*` YasinHub is the documented binding exception because the PWA/dashboard must remain reachable through the Hub server. Lifecycle health checks still target `127.0.0.1`.

The canonical allocation is maintained in YasinHub's `yasinhub/ports.py`. The service registry consumes that allocation for lifecycle configuration.

## 3. Portless services

The following are not assigned HTTP ports:

```text
YasinRelay       -> portless worker
                 launcher: .venv/bin/yasinrelay-termux run --schedule --non-interactive
                 process_pattern: yasinrelay.cli

eitaa_news_v2    -> retired worker
backup_manager   -> retired worker
```

A worker must not receive an artificial HTTP port merely to participate in lifecycle management.

## 4. Process Identity and Port Ownership

A listening port does not by itself prove service identity. For an HTTP lifecycle operation, YasinHub verifies:

```text
Process Identity
+
Port Ownership
+
Health
```

Process identity is checked from OS process information. Port ownership is checked against the expected process where the platform permits owner discovery.

On platforms where direct socket-owner discovery is unavailable, the implementation may use the documented correlated verification path (free-before-spawn, expected-port occupancy, and a succeeding contract health endpoint). If neither an owner proof nor the required health anchor is available, the result is fail-closed.

## 5. Unknown-owner rule

```text
UNKNOWN PORT OWNER -> FAIL CLOSED
```

If an expected Yasin port is already occupied by an unrelated process:

- do not kill it;
- do not terminate it;
- do not reuse its PID;
- do not report the Yasin service as `RUNNING`;
- fail the lifecycle operation;
- diagnostics may record the port/PID needed to diagnose the collision, but never secrets.

Only a process that YasinHub itself has safely identified as the managed service may be stopped during lifecycle recovery.

## 6. Start contract

A service is `RUNNING` only when all conditions hold:

```text
Process is alive
AND
Process identity matches expected service
AND
Expected port is owned by that process/service
AND
Health endpoint succeeds
```

PID existence or successful process creation alone is insufficient.

## 7. Stop and restart contract

Restart follows this sequence:

```text
1. Identify current service PID
2. Verify Process Identity
3. Gracefully stop
4. Verify old PID is dead
5. Verify expected port is released
6. Start service
7. Obtain new PID
8. Verify new Process Identity
9. Verify expected port ownership
10. Verify HTTP health
11. Only then report RUNNING
```

The old PID must never be treated as proof of the new runtime. This protects against stale state and PID reuse.

## 8. Wrong-port rule

If the expected process is alive and identity-matching but serves on a port other than its canonical allocation, the service is not `RUNNING`.

Example:

```text
expected: 7001
actual:   7002
result:   FAIL CLOSED
```

## 9. Host binding

Local Yasin HTTP services should bind to:

```text
127.0.0.1
```

unless the architecture explicitly requires external reachability. Such exceptions must be documented. The current YasinHub `0.0.0.0` binding is the documented PWA/dashboard exception.

## 10. Single Control Plane

YasinHub remains the sole Control Plane, lifecycle authority, and PID authority.

Canonical lifecycle paths remain:

```text
PWA  -> YasinHub
CLI  -> YasinHub
```

The PWA must not directly manage processes or ports. No second Control Plane, PID manager, or authorization system is introduced by this port contract.

## 11. Registry and compatibility

The runtime registry is the lifecycle source of truth for service configuration. It must expose, where applicable:

```text
service_name
canonical_path
start_command
process_pattern
host
port
health_endpoint
```

Legacy ecosystem-path compatibility remains supported where required. The canonical runtime root is:

```text
~/YasinEco
```

This contract does not supersede or regress the canonical-root correction from YasinHub commit `b7b13bb`.

## 12. Migration rule

Legacy bindings such as `8000`/`8080`/`8101` are not canonical allocations for HTTP services after Issue #179. Transitional environment overrides may remain where already supported for backward compatibility, but new canonical configuration must use the allocation in this document.

Do not change a service's port as an ad-hoc fix without updating the canonical registry and this contract.

## 13. Security rules

- Never log tokens or API keys.
- Never expose `.env` contents.
- Never kill an unknown port owner.
- Do not perform broad unnecessary port scanning.
- Probe only expected service ports during lifecycle verification.
- Keep lifecycle authority in YasinHub.
- Fail closed when ownership or identity cannot be established safely.

## 14. Evidence and testing

YasinHub Issue #179 defines the required automated coverage for:

- canonical allocation and uniqueness;
- reserved-range validation;
- portless Relay behavior;
- unknown-owner collision handling;
- protection against killing foreign processes;
- Process Identity verification;
- Port Ownership verification;
- health verification;
- PID-death and port-release verification;
- restart/new-PID verification;
- wrong-port rejection.

Runtime claims require runtime evidence. Source inspection alone is not a substitute for process, port, health, or browser evidence where those are required.

## 15. Authority

This document is the YASIN-DOCS cross-repository statement of the Issue #179 port contract. The executable allocation and lifecycle enforcement remain implemented by YasinHub.
