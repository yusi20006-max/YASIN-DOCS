# YasinCLI — Project Architecture Record

## Identity

- Repository: `yusi20006-max/Yasin-cli`
- Documented implementation branch in README: `initial-setup`
- Technology: Node.js
- Role: modular ecosystem/developer command-line tool

## Capability Model

```text
Configuration
Doctor / diagnostics
Status
Service manager
Plugin system
```

## Module Map

```text
src/index.js
src/config/ConfigManager.js
src/core/Command.js
src/core/CommandRegistry.js
src/commands/config.js
src/commands/doctor.js
src/commands/status.js
src/commands/service.js
src/commands/plugin.js
src/services/ServiceManager.js
src/plugins/PluginSystem.js
```

## Responsibilities

- hierarchical JSON configuration
- custom argument/option parsing and command registry
- environment diagnostics and optional auto-healing
- process/resource status
- cross-platform background service lifecycle
- dynamic plugin installation/enable/disable/uninstall

## Architectural Boundary

YasinCLI is a control/developer interface. It should not absorb the business logic of YasinFeed/YasinPress, agent execution internals, or Hub status storage. Cross-project integration should happen through explicit interfaces.

## Testing

The README documents Jest unit/integration tests and `npm test`.

## Audit Status

**Level 3:** command/module architecture is documented. Exact current branch state, package dependencies, Core/Hub integration contracts and service persistence model require source audit.
