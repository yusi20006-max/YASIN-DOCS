# Yasin Ecosystem — AI Onboarding

## Purpose

Entry point for a new AI coding agent working on the Yasin ecosystem. Read this before modifying code.

## 1. What Yasin Is

Yasin is a multi-repository software ecosystem, not one monolithic application. Its projects provide runtime foundations, agents, AI capabilities, management, relay/content processing, publishing, developer tooling, and centralized documentation.

Treat each repository as a bounded component. Do not invent cross-project coupling.

## 2. Reading Order

```text
1. YASIN-DOCS/README.md
2. Project Registry
3. Master Architecture
4. Per-project architecture records
5. System Graphs
6. Evidence/audit documents
7. AI documentation
```

Use the repository index when filenames evolve.

## 3. Ecosystem Mental Model

```text
Foundation:       Yasin-Core → Yasin-Agent
Intelligence:     Yasin-AI
Management:       YasinHub
Content/Relay:    YasinRelay → YasinFeed / publishing
News:             YasinPress
Operations:       YasinCLI
Developer tools:  TJC
Knowledge:        YASIN-DOCS
```

This is conceptual. A concrete dependency requires evidence.

## 4. Project Selection

Before editing, identify the owner:

- runtime/foundation → Yasin-Core
- agent/task behavior → Yasin-Agent
- AI/knowledge/provider behavior → Yasin-AI
- management/status → YasinHub
- relay/ingestion/pipeline → YasinRelay
- feed generation/publishing → YasinFeed
- news/press processing → YasinPress
- ecosystem operator CLI → YasinCLI
- developer/Jules automation → TJC
- architecture/documentation → YASIN-DOCS

If ownership is ambiguous, inspect dependency and contract documents first.

## 5. Evidence Levels

- **Verified** — directly supported by source/configuration.
- **Documented** — stated by project documentation.
- **Inferred** — derived from verified evidence.
- **Candidate** — plausible but unverified.
- **Unknown** — insufficient evidence.

Never promote Candidate or Unknown to Verified by assumption.

## 6. Safe Change Loop

```text
Understand request
  ↓
Select owning repository
  ↓
Read local README + architecture
  ↓
Inspect source/config/tests
  ↓
Map dependencies/contracts
  ↓
Assess cross-project impact
  ↓
Implement smallest correct change
  ↓
Run focused tests
  ↓
Run broader validation
  ↓
Update architecture docs if needed
  ↓
Review diff
  ↓
Report exact result
```

## 7. Cross-Project Change Rule

If a change modifies a public API, message schema, storage schema, configuration contract, lifecycle behavior, or runtime boundary, inspect every documented consumer before finalizing.

## 8. Do Not Assume

Do not assume:

- every repository is a deployable service;
- every module is public;
- every JSON object is a stable schema;
- every event is ecosystem-wide;
- a CLI owns the process it controls;
- SQLite databases are shared;
- deployment uses Docker/Kubernetes/systemd;
- an undocumented endpoint exists;
- an import search miss proves no dependency exists.

## 9. Code vs Documentation

Source/configuration is stronger evidence for implementation reality. If code and docs disagree, record the discrepancy and update the authoritative documentation rather than silently inventing behavior.

## 10. Completion Standard

Verify intended behavior, tests, public contracts, configuration, security implications, backward compatibility, affected documentation, and repository diff.

## 11. Handoff Format

```text
Repository
Branch
Task
Files changed
Behavior changed
Tests run
Tests passed/failed
Architecture impact
Documentation updated
Known limitations
Next recommended step
```

## Golden Rule

**Understand the boundary before changing the implementation.**
