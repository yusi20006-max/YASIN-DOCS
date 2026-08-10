# Yasin Ecosystem — ADR Index v1

## Purpose

Canonical index of Architecture Decision Records and decisions established during the ecosystem architecture audit.

## ADR-001 — Public API First

**Status:** Accepted

Cross-project consumers must depend on public SDK/API contracts, not private implementation modules.

## ADR-002 — Core as Shared Runtime Foundation

**Status:** Accepted

Yasin-Core owns shared runtime primitives, execution, provider abstraction, API gateway, security, storage abstractions, and ecosystem compatibility.

## ADR-003 — Registry Does Not Imply Dependency

**Status:** Accepted

Presence of a project in YasinHub/registry/documentation does not establish a runtime dependency. Dependency status requires source, adapter, or executable integration evidence.

## ADR-004 — Explicit Dependency Evidence

**Status:** Accepted

Dependency claims use four evidence classes: `VERIFIED`, `DOCUMENTED`, `PLANNED`, and `NOT CONFIRMED`. When evidence is insufficient, `NOT CONFIRMED` is mandatory.

## ADR-005 — Contract Ownership

**Status:** Accepted

Every public contract has one canonical owner. Consumers must not redefine or silently fork another project's contract.

## ADR-006 — Memory and Persistence Isolation

**Status:** Accepted

Core memory, Agent session state, AI platform memory, and application-local persistence remain independently owned unless an explicit shared contract is introduced.

## ADR-007 — Provider-Neutral Boundaries

**Status:** Accepted

An AI/content provider abstraction does not itself establish a dependency on Yasin-AI or another specific provider. Concrete adapters must establish that dependency explicitly.

## ADR-008 — Core Compatibility Ownership

**Status:** Accepted

Ecosystem compatibility is a Core responsibility where Core validators already exist. Project-specific compatibility rules must not contradict the canonical Core mechanism.

## ADR-009 — YasinCLI Adapter Isolation

**Status:** Accepted

YasinCLI must operate through public project contracts/adapters and must not directly manipulate another project's private database, internal modules, or process state.

## ADR-010 — Breaking Change Gate

**Status:** Accepted

A breaking cross-project contract change requires an ADR, Contract Registry update, compatibility validation, migration notes, integration tests, and release documentation.

## ADR-011 — Evidence Before Production Claims

**Status:** Accepted

Architecture documentation must not claim full integration verification, ecosystem compatibility, or production readiness without executable evidence.

## ADR-012 — Architecture Gate Policy

**Status:** Accepted

The current ecosystem architecture is **CONDITIONAL PASS**. Architecture/governance are sufficiently defined, while runtime compatibility, YasinCLI implementation, and final end-to-end smoke testing remain open gates.

## Decision Map

```text
ADR-001  Public API First
    │
    ├── ADR-005 Contract Ownership
    └── ADR-009 CLI Adapter Isolation

ADR-002  Core Foundation
    │
    ├── ADR-007 Provider Neutrality
    └── ADR-008 Compatibility Ownership

ADR-003  Registry ≠ Dependency
    │
    └── ADR-004 Evidence Classes

ADR-006  State Isolation

ADR-010  Breaking Change Gate
    │
    └── Contract Registry + Tests

ADR-011  Evidence Before Claims
    │
    └── ADR-012 Architecture Gate
```

## Governance Rule

Any future architectural change that modifies dependency direction, ownership, public API, memory boundaries, compatibility semantics, or control-plane/runtime boundaries must add or update an ADR before the Contract Registry is considered final.

## Status

**ADR Index v1 — consolidated decision baseline complete.**
