# TJC — Project Architecture Record

## Evidence Level

**README-verified / source audit pending**

## Identity

Repository: `yusi20006-max/TJC`

## Purpose

TJC (Termux Jules CLI) is a POSIX-shell-based CLI platform for Google Jules API workflows, designed for standard Linux and Android via Termux.

## Architectural Scope

TJC is developer automation/tooling rather than a Yasin runtime component. It provides a reusable command-line automation platform around Jules workflows.

## Major Subsystems

### Workflow Engine

- YAML/JSON workflow declarations
- strict validation
- modular execution steps
- command-line execution
- execution history and JSON reports

Documented commands include:

```text
tjc workflow run <file.yml>
tjc workflow list
tjc workflow show <report_file.json>
```

### Scheduler

The scheduler is designed around non-daemon execution and integration with:

- cron
- Termux:Boot
- Termux:Tasker

Documented commands include:

```text
tjc schedule add
 t jc schedule list
 t jc schedule remove
 t jc schedule run
 t jc schedule run-pending
 t jc schedule history
```

(Exact command parsing and implementation must be verified from source.)

### Plugin / Extension System

The project documents a plugin system for custom workflow steps and CLI commands.

### Testing

TJC has a dedicated testing and verification guide and linting/assertion framework according to the repository documentation.

## Security Boundary

Workflow declarations are documented as strictly validated to reduce command injection and directory traversal risks. The implementation must still be audited before treating these protections as complete security guarantees.

## Ecosystem Relationship

TJC is primarily developer tooling. It can support development and automation of the Yasin ecosystem, but it should not be modeled as a runtime dependency of Yasin-Core, Yasin-Agent, or application services without explicit implementation evidence.

## Audit Remaining

- Shell/module structure
- Jules API boundary
- Authentication/secrets
- Workflow parser/validator implementation
- Scheduler persistence
- Plugin loading and trust model
- Test framework details
- CI/CD
- Compatibility matrix
- Exact Yasin ecosystem integrations
