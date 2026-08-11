# Yasin AI Authentication Extension v1

**Status:** Proposed
**Scope:** Yasin-AI and any Yasin component that consumes AI models
**Type:** Cross-provider authentication extension

## Purpose

Define a provider-independent authentication layer so Yasin can access AI providers through more than static API keys. Authentication must be an abstraction owned by Yasin rather than embedded in individual providers.

## Core Model

```text
Yasin AI
   |
   v
AI Provider Manager
   |
   v
Credential / Auth Manager
   |
   +-- API Key
   +-- OAuth 2.0
   +-- Service Account / Application Credentials
   +-- Access Token / Refresh Token
   +-- Local / No-auth
   |
   v
Provider Adapter
   |
   v
AI Model
```

## Supported Authentication Classes

### API Key

For providers that expose API-key authentication.

### OAuth 2.0

For providers such as Google where user authorization can be used instead of a manually managed API key. OAuth credentials must be stored separately from provider configuration and refreshable tokens must be handled by the credential manager.

### Service/Application Credentials

For server-to-server integrations where the provider supports application credentials or service accounts.

### Access/Refresh Tokens

The credential layer must support short-lived access tokens and their associated refresh mechanism without exposing raw tokens to application code.

### Local / No Authentication

For local model runtimes such as llama.cpp or Ollama when authentication is disabled or handled locally.

## Google Example

Google/Gemini must not be modeled as API-key-only.

```text
Google Gemini
  |
  +-- API Key
  +-- OAuth 2.0
  +-- Application / Service Credentials (where supported)
```

OAuth is an authentication/authorization mechanism. It does **not** imply free or unlimited model usage; quota, model access, billing, and provider policy remain independent concerns.

## Provider Abstraction

A provider definition should declare supported authentication methods rather than implementing credential storage itself.

Example conceptual configuration:

```yaml
provider: google-gemini
auth:
  supported:
    - oauth2
    - api_key
```

```yaml
provider: openai
auth:
  supported:
    - api_key
```

```yaml
provider: local-llama-cpp
auth:
  supported:
    - none
    - local
```

## Architectural Rules

1. Provider adapters must not own persistent credentials.
2. Application code must not directly manipulate OAuth refresh tokens.
3. Auth selection must happen through the Credential/Auth Manager.
4. Authentication state must be independent from model routing.
5. Provider routing, quota, billing, and authentication are separate concerns.
6. Secrets must never be written to normal logs, prompts, memory, or telemetry.
7. Local providers must be first-class providers rather than special cases in Agent code.
8. Adding a new authentication mechanism should not require changes to Yasin Agent business logic.

## Relationship to AI Routing

The authentication layer is designed to sit below provider routing:

```text
Yasin Agent
    |
    v
AI Router
    |
    v
Provider Manager
    |
    v
Auth Manager
    |
    v
Provider Endpoint
```

This allows Yasin to combine authentication with the provider-pool and fallback architecture used elsewhere in the ecosystem.

## Security Requirements

- Encrypt or otherwise securely protect stored credentials where practical.
- Use OS/device credential storage when available.
- Minimize token lifetime and scope.
- Refresh tokens only through the credential manager.
- Redact secrets from errors and logs.
- Never place credentials in Git repositories, prompts, memory records, or issue descriptions.

## Evidence / Reference

This extension is a **proposed Yasin architecture** inspired by the need to support multiple provider authentication mechanisms, including Google OAuth, rather than requiring API keys for every provider.

Provider-specific implementation details must be verified against the provider's current official documentation before implementation.

## Future Integration Points

Potential integration targets:

- Yasin-AI Provider Manager
- Yasin-Agent model selection
- YasinCLI credential commands
- YasinHub provider/credential observability
- OmniRoute-style provider routing
- Local runtimes such as llama.cpp and Ollama

## Non-Goals

This document does not define provider-specific quotas, pricing, model capabilities, or a universal credential vault implementation. Those belong in provider documentation and implementation-specific security/operations documents.
