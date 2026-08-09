# Yasin Ecosystem — System Overview

## Purpose

This document provides a compact architectural map for humans and AI agents before they read the full Master Architecture.

## Conceptual Layers

```text
┌─────────────────────────────────────────────┐
│ Users / Developers / Operators              │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│ Control / Management                       │
│ YasinCLI · YasinHub                        │
└──────────────────────┬──────────────────────┘
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
┌─────────────────────┐ ┌─────────────────────┐
│ Agent / Runtime     │ │ Applications        │
│ Yasin-Agent         │ │ YasinFeed           │
│ Yasin-Core          │ │ YasinPress          │
└──────────┬──────────┘ └──────────┬──────────┘
           │                       │
           └──────────┬────────────┘
                      ▼
┌─────────────────────────────────────────────┐
│ AI / Integration / Transport                │
│ Yasin-AI · YasinRelay · OpenFeed · FeedBridge│
└─────────────────────────────────────────────┘

YASIN-DOCS sits beside these layers as the ecosystem-level
architecture and knowledge source, not as a runtime service.
```

## Important Boundary

This diagram is conceptual. A direct arrow must not be interpreted as a verified runtime dependency until the corresponding repository audit establishes it.

## Source of Detail

For full rules, evidence status, unresolved questions, and AI operating guidance, see `MASTER_ARCHITECTURE.md`.
