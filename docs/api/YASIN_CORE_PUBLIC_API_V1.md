# Yasin-Core — Public SDK/API Surface v1

## Evidence

Source-verified against `yusi20006-max/Yasin-core` README, `yasin_core/sdk/__init__.py`, and `yasin_core/sdk/client.py`.

Current validated repository version: **3.3.0**. fileciteturn191file0

## 1. Role

Yasin-Core is the central runtime and shared backend foundation of the Yasin ecosystem. Its documented responsibilities include execution, runtime, context, memory, API, security, compatibility, SDK, storage, plugin/provider integration, and observability. fileciteturn191file0

## 2. Public SDK Export Surface

`yasin_core.sdk.__init__` explicitly exports a broad public surface.

### Primary client/runtime

```text
YasinCoreClient
AsyncYasinCoreClient
RuntimeOrchestrator
RuntimeState
OrchestratorError
```

### Agents/tasks/tools

```text
BaseAgent
Task
IAgentRuntime
AgentRuntime
BaseTool
FunctionTool
tool
ToolRegistry
ToolManager
```

### Context/events

```text
active_context
get_current_context
RuntimeContext
ContextEngine
Event
EventBus
```

### Storage

```text
BaseStorage
JSONFileStorage
InMemoryStorage
StorageError
StorageConnectionError
StorageNotFoundError
StorageValidationError
get_storage
register_backend
```

### Execution

```text
Job
ExecutionTask
JobStatus
JobPriority
TaskExecutionEngine
Scheduler
ScheduledJob
WorkerState
WorkerNode
BaseDistributedWorker
DistributedWorkerManager
```

### Providers

```text
AIProvider
AIChatMessage
AIRequest
AIResponse
AIResponseChunk
AIProviderError
AIProviderConnectionError
AIProviderAuthError
AIProviderRateLimitError
ProviderRegistry
ProviderManager
MockProvider
LocalProvider
OpenAICompatibleProvider
```

### API Gateway

```text
APIRequest
APIResponse
APIError
APIErrorCode
BaseAuthenticator
APIKeyAuthenticator
APIGateway
```

### Security

```text
SecurityError
AccessDeniedError
AuthenticationError
PermissionValidationError
Permission
Role
Subject
BasePolicy
DefaultRBACPolicy
PolicyEngine
ConfigurationSecurityValidator
SensitiveDataProtector
BaseCredentialStore
InMemoryCredentialStore
AuditLogger
SecurityManager
require_permission
```

### SDK v2 contracts

```text
SDKError
SDKValidationError
SDKAuthenticationError
SDKConnectionError
SDKExecutionError
SDKDeprecationWarning
translate_core_errors
SDKRequest
SDKResponse
ISDKClient
ISDKAuthenticator
SDKVersionChecker
deprecated
SDKMigrationHelper
```

### Compatibility

```text
Version
is_compatible
VersionNegotiator
APICompatibilityChecker
DeprecationManager
LegacyAPIAdapter
SchemaMigrator
ConfigurationMigrator
DataMigrator
AgentCompatibilityValidator
HubCompatibilityValidator
RelayCompatibilityValidator
CLICompatibilityValidator
RuntimeCompatibilityChecker
CompatibilityManager
CompatibilityError
VersionMismatchError
APICompatibilityError
MigrationError
EcosystemValidationError
```

All of the above are source-verified exports from `yasin_core/sdk/__init__.py`. fileciteturn193file0

## 3. YasinCoreClient Contract

### Constructor

Source-verified constructor:

```python
YasinCoreClient(
    short_term_memory=None,
    long_term_memory=None,
    service_registry=None,
    context_engine=None,
    di_container=None,
    config_manager=None,
    storage=None,
    api_gateway=None,
)
```

The client initializes the core runtime services, including event bus, agent manager/executor, AgentRuntime, plugin registry, provider manager, tool manager, context engine, DI container, configuration manager, observability, execution engine, scheduler, distributed workers, orchestrator, security manager, compatibility manager, storage, and API gateway. fileciteturn194file0

## 4. SDK v2 Namespaces

The client implements grouped namespaces for major domains.

### `agents`

Source-verified operations:

```python
agents.register(agent: BaseAgent) -> None
agents.get(name: str) -> Optional[BaseAgent]
agents.remove(name: str) -> Optional[BaseAgent]
agents.list() -> List[str]
agents.start() -> None
agents.stop() -> None
```

### `tasks`

```python
tasks.create(id: str, name: str, input_data: Optional[Dict[str, Any]] = None) -> Task
tasks.execute(task: Task) -> Task
tasks.submit_job(job: Job) -> Job
tasks.create_job(
    target: Any,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
    name: Optional[str] = None,
    priority: int = 20,
    retries: int = 0,
    timeout: Optional[float] = None,
) -> Job
tasks.get_job(job_id: str) -> Optional[Job]
tasks.cancel_job(job_id: str) -> bool
```

### `memory`

```python
memory.save(
    key: str,
    value: Any,
    category: str = "short-term",
    metadata: Optional[Dict[str, Any]] = None,
    ttl: Optional[int] = None,
) -> None

memory.get(
    key: str,
    default: Any = None,
    category: str = "short-term",
) -> Any
```

### `context`

```python
context.create(data: Optional[Dict[str, Any]] = None)
context.active
```

### `tools`

```python
tools.register(tool: BaseTool) -> None
tools.get(name: str) -> Optional[BaseTool]
tools.remove(name: str) -> Optional[BaseTool]
tools.list() -> List[str]
tools.execute(name: str, *args: Any, **kwargs: Any) -> Any
```

These namespace methods are source-verified in `client.py`. fileciteturn194file0

## 5. Lifecycle Contract

The client exposes initialization and lifecycle behavior:

```python
initialize() -> None
is_active() -> bool
__enter__() -> YasinCoreClient
__exit__(exc_type, exc_val, exc_tb) -> None
```

The constructor performs automatic initialization for backward compatibility. `initialize()` initializes storage once. Context-manager entry initializes and starts the client; exit stops it. fileciteturn194file0

## 6. Memory Ownership Boundary

Yasin-Core explicitly supports:

```text
ShortTermMemory
LongTermMemory
StorageBackedLongTermMemory
```

The client defaults to in-memory short-term and long-term memory unless the supplied storage advertises persistence, in which case storage-backed long-term memory is selected. fileciteturn194file0

This establishes **Core-owned runtime memory**, which must not be confused with:

```text
Yasin-Agent session memory
Yasin-AI platform memory
project-local Feed/Press/Relay storage
```

Cross-project memory sharing requires an explicit contract.

## 7. Provider Boundary

Yasin-Core exports a provider-neutral abstraction:

```text
AIProvider
AIRequest
AIResponse
AIResponseChunk
ProviderRegistry
ProviderManager
```

and concrete adapters including:

```text
MockProvider
LocalProvider
OpenAICompatibleProvider
```

Therefore the canonical Core architecture is:

```text
Consumer
   ↓
Yasin-Core Provider API
   ↓
Provider implementation
```

rather than hard-coding a single model vendor into runtime code. fileciteturn193file0

## 8. Execution Boundary

The public SDK exposes:

```text
Job
ExecutionTask
JobStatus
JobPriority
TaskExecutionEngine
Scheduler
ScheduledJob
WorkerState
WorkerNode
BaseDistributedWorker
DistributedWorkerManager
```

The client also provides job creation/submission/cancellation through the Task namespace. This establishes execution as a Core-owned capability rather than a responsibility of YasinHub or YasinCLI.

## 9. API Gateway Boundary

Core publicly exports:

```text
APIRequest
APIResponse
APIError
APIErrorCode
BaseAuthenticator
APIKeyAuthenticator
APIGateway
```

This is the canonical API gateway boundary exposed by Core's public SDK package.

## 10. Security Boundary

Security is also part of the public Core surface, including RBAC/policy, authentication, credential storage, auditing, sensitive-data protection, and permission enforcement.

Consumers should prefer these abstractions rather than implementing parallel security mechanisms inside the Core runtime.

## 11. Compatibility Contract

The public SDK exposes compatibility validators specifically named for ecosystem components:

```text
AgentCompatibilityValidator
HubCompatibilityValidator
RelayCompatibilityValidator
CLICompatibilityValidator
RuntimeCompatibilityChecker
```

This is strong source evidence that ecosystem compatibility is an intentional Core responsibility.

The generic compatibility API includes:

```text
Version
is_compatible
VersionNegotiator
APICompatibilityChecker
CompatibilityManager
```

## 12. Ecosystem Dependency Direction

The source-backed architecture supports:

```text
                  Yasin-Core
                 /    |    \
                /     |     \
           Agent     Hub     Relay
                \     |     /
                 \    |    /
                  YasinCLI
```

The exact operational direction for each command remains project-specific, but Core is the shared runtime/API/compatibility foundation.

## 13. Contract Status Update

```text
CORE-SDK public exports       🟢 Source Verified
CORE-CLIENT constructor      🟢 Source Verified
CORE v2 namespaces           🟢 Source Verified
CORE memory boundary         🟢 Source Verified
CORE provider boundary       🟢 Source Verified
CORE execution boundary      🟢 Source Verified
CORE API gateway             🟢 Source Verified
CORE security surface        🟢 Source Verified
CORE compatibility surface   🟢 Source Verified
```

## 14. Architectural Corrections

This audit resolves a previous uncertainty around the Core SDK.

The following are **real public exports**, not assumptions:

```text
YasinCoreClient
AsyncYasinCoreClient
BaseAgent
BaseTool
AgentRuntime
RuntimeOrchestrator
ProviderManager
APIGateway
Scheduler
CompatibilityManager
```

The earlier generic distinction between "possible API names" and verified API names should therefore be replaced with this source-backed inventory.

## 15. AI Agent Rules

When modifying Yasin-Core:

1. Treat `yasin_core.sdk` as the primary public SDK surface.
2. Preserve exported symbols unless a deliberate breaking API change is approved.
3. Prefer SDK namespaces over direct internal manager access.
4. Keep provider implementations behind `AIProvider` abstractions.
5. Keep execution and scheduling under Core ownership.
6. Preserve compatibility validators for ecosystem projects.
7. Do not create project-specific copies of Core runtime functionality.
8. Update this document whenever public exports or signatures change.
9. Update the Contract Registry for cross-project API changes.
10. Use an ADR for breaking changes or new dependency directions.

## 16. Open Work

The next depth of Core audit should extract:

```text
AsyncYasinCoreClient signatures
remaining YasinCoreClient methods
SDKRequest / SDKResponse schemas
APIRequest / APIResponse schemas
provider request/response behavior
compatibility return/error semantics
security authorization semantics
storage interface signatures
execution lifecycle/state transitions
```

The current document is already a **source-verified public surface inventory**, but not yet a complete behavioral specification.

## Status

**Yasin-Core Public SDK/API v1 — source-verified baseline complete.**
