# YasinCoder Architecture

**Evidence state:** Confirmed for repository boundaries and current implementation; target for planned first-run/provider expansion.

## Product role

YasinCoder is the ecosystem's coding-agent product. It owns coding-agent orchestration, project/workspace intelligence, coding tools, provider abstraction, execution policy, sessions, and its user-facing web/PWA surface.

Yasin-AI remains the canonical ecosystem AI capability platform. YasinCoder must not silently depend on Yasin-AI private runtime state. Any future integration must use an explicit public/versioned contract.

## Runtime architecture

```text
User / PWA
    |
    v
Application API / Universal Gateway
    |
    +--> Routing & policy
    |       |
    |       +--> Local/offline provider
    |       |       +--> user-selected runtime/model
    |       |
    |       +--> Online provider
    |               +--> Gemini / compatible / custom API
    |
    +--> Coding Agent Engine
            |
            +--> Workspace / project services
            +--> File/search/edit tools
            +--> Git tools
            +--> Test/build tools
            +--> Permission & sandbox policy
```

## First-run AI contract

The user chooses the operating mode at first run:

1. **Offline / local AI** — configure a local runtime such as llama.cpp, Ollama, or another compatible endpoint, then register the user's own model.
2. **Online AI** — choose a supported provider/model and enter only the credentials/configuration required by that provider.

The repository never bundles the developer's GGUF/model and never requires a particular model name, absolute path, device path, or local port.

## Model portability

GGUF is a model-file format, not an application dependency. A llama.cpp runtime can serve different GGUF models. Therefore YasinCoder stores portable provider/model configuration rather than shipping a specific model. Runtime data, credentials, downloaded models, caches and logs remain outside Git.

## Repository boundaries

- `core/`: reusable project intelligence and domain services.
- `commands/`: user operations and orchestration.
- `providers/`: provider adapters.
- `docs/`: project implementation and operational documentation.
- `tests/`: deterministic and integration verification.
- User/runtime state: outside Git.

## Security boundary

Default deployments are local/localhost oriented. Shell execution, network-enabled tools, Git mutation, remote access and other sensitive capabilities require explicit policy and sandbox controls. Secrets must never be committed, logged, exposed through UI responses, or copied into documentation.

## Testing boundary

Deterministic CI must not require private API credentials or a specific local model. Real-provider tests are environment-dependent and may be manual. Gemini availability can fail because of account quota even when the CLI and gateway routes are correctly installed.

## Clean-clone invariant

A new user must be able to clone YasinCoder, install it, select a different local model or online provider, and operate without access to the developer's machine, credentials, model files, runtime state, or local backups.
