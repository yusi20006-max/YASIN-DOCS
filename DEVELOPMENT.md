# Yasin Ecosystem Development Guide

This document defines the high-level development approach for the documentation ecosystem. Repository-specific development instructions belong in the corresponding project repository and project document.

## Core Workflow

```text
Understand the issue
    -> Identify the owning project/layer
    -> Inspect current implementation
    -> Check cross-project impact
    -> Make the smallest appropriate change
    -> Test
    -> Review documentation impact
    -> Commit / PR
```

## Architectural Rule

Before implementing a feature, determine which project owns the responsibility. Do not move functionality between repositories merely because doing so is convenient.

## Current vs Planned

Documentation must use explicit language for:

- implemented behavior;
- verified but incomplete behavior;
- proposed architecture;
- roadmap items;
- experimental behavior.

## Cross-Repository Changes

When a change crosses a project boundary, the developer should inspect both sides of the interface and document any changed contract, dependency, configuration, or operational requirement.

## Quality Expectations

Important projects should maintain appropriate unit, integration, contract, smoke, and end-to-end tests according to their role. CI results should be considered part of the evidence for implementation status.
