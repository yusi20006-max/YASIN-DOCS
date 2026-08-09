# Phase 5 — Per-Project Audit Template

Every active project should eventually reach the same documentation depth.

## 1. Identity

Repository, URL, default branch, version, visibility, license, ownership.

## 2. Purpose

What problem it solves and its primary users.

## 3. Responsibilities

What it owns and what it explicitly does not own.

## 4. Architecture

Runtime model, layers, modules, entry points and lifecycle.

## 5. Public Interfaces

CLI, Python/Node APIs, HTTP APIs, files, events, SDKs and contracts.

## 6. Dependencies

Runtime, build, optional and external dependencies.

## 7. Consumers

Projects/services/tools that depend on it.

## 8. Data

Storage, schemas, queues, cache, persistence and migrations.

## 9. Configuration

Files, environment variables, defaults, secrets and precedence.

## 10. Integrations

AI providers, Telegram, Eitaa, GitHub/Jules, storage and other services.

## 11. Testing

Unit/integration/e2e tests, fixtures, coverage and commands.

## 12. CI/CD

Workflows, checks, release process and deployment.

## 13. Security

Trust boundaries, secrets, authentication, authorization, sandboxing and untrusted input.

## 14. Operations

Startup, shutdown, scheduling, health checks, logging, backup and recovery.

## 15. Repository Governance

Issues, PRs, milestones, releases, branches and documented roadmap.

## 16. Cross-Project Impact

Producers, consumers, contracts, blast radius and required documentation updates.

## 17. Evidence

Every non-obvious architectural claim should point to source/configuration/test evidence.

## 18. Audit Level

Use the Yasin architecture maturity model from `MASTER_ARCHITECTURE.md`.
