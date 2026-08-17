# ADR-0012: Yasin-Operations Boundary and Optional Integration

- Status: Accepted
- Date: 2026-08-17
- Decision owners: Yasin ecosystem maintainers
- Scope: Yasin-Operations and its relationship to the rest of the ecosystem
- Supersedes: None
- Superseded by: None

## Context

A new repository, `yusi20006-max/Yasin-Operations`, has been created as a modular Operations Agent for the Yasin ecosystem: operations, diagnostics, health checks, service lifecycle management, runtime inspection, operational tooling, and optional adapters/integrations.

Its introduction requires an explicit boundary decision so it does not silently become a required runtime dependency of any existing project, and so its relationship to Hermes and Yasin-AI is documented before any integration work begins.

## Decision

1. Yasin-AI remains the Canonical AI Platform. Yasin-Operations does not own Core AI capabilities.
2. YasinPress remains the owner of the publishing/news-processing domain.
3. YasinRelay remains the owner of relay/feed transport responsibilities.
4. Hermes is documented as a possible future operator/interface for Yasin-Operations, not a current integration.
5. Yasin-Operations must be independently deployable and independently testable.
6. The absence or shutdown of Yasin-Operations must not break Yasin-AI, YasinPress, YasinRelay, or Hermes.
7. No mandatory cross-repository dependency is created by this decision, in either direction.
8. The future integration direction Hermes -> Yasin-Operations -> Yasin-AI is documented as a planned/optional relationship only. It is explicitly **not** an implemented integration as of this ADR.
9. Any future Yasin-AI integration from Yasin-Operations must go through Yasin-AI's public, versioned contracts (`yasinai.contracts` / `yasinai.services`), consistent with the integration policy documented in Yasin-AI (see `docs/projects/YASIN_AI.md` and Yasin-AI's `yasinai/integration/__init__.py` policy statement).
10. Any future Hermes integration must be implemented through an adapter, not a hard dependency.

## Rationale

The ecosystem's existing architectural principle (see `ECOSYSTEM.md`) is that each project has a clear primary responsibility and boundary. Introducing an operations-focused project creates real value (centralized diagnostics/health/lifecycle tooling) without requiring any existing project to adopt it as a dependency. Keeping the integration direction and boundary explicit from the start prevents the kind of undocumented coupling this ecosystem's ADRs and registry rules are designed to avoid.

## Alternatives Considered

### Make Yasin-Operations a required control-plane component
Rejected. This would duplicate/compete with YasinHub's existing management/status role and would violate the registry rule against inferring dependencies without evidence.

### Fold operations tooling into Hermes directly
Rejected for this decision. Hermes' relationship to Yasin-Operations is left as a future optional adapter rather than an immediate merge of responsibilities, preserving both projects' independence.

### Treat Yasin-Operations as owning AI capabilities
Rejected. Yasin-AI remains the Canonical AI Platform per existing ADR-001-YASIN-AI-CANONICAL-AI-PLATFORM.md; this ADR does not change that.

## Consequences

Yasin-Operations is registered in `PROJECT_REGISTRY.md` / `PROJECT_REGISTRY.yaml` with `status: newly-registered`, `architecture_status: provisional`, and empty `depends_on`/`consumers`, consistent with registry rules that require source-level evidence before promoting relationships.

Future work that implements the Hermes -> Yasin-Operations -> Yasin-AI direction must update this ADR's status and the registry's `depends_on`/`consumers` fields with source-level evidence at that time, not before.

## Evidence

- `yusi20006-max/YASIN-DOCS` Issue #27
- `docs/audits/ACTIVITY_LOG_2026-08-17.md`
- `docs/projects/PROJECT_REGISTRY.md`
- `docs/projects/PROJECT_REGISTRY.yaml`

## Related Documents

- ADR-0001-yasin-multi-repository-ecosystem.md
- ADR-001-YASIN-AI-CANONICAL-AI-PLATFORM.md
- ADR-0004-yasinhub-management-boundary.md
- ADR-0011-documentation-governance.md

## Open Questions

- What adapter interface will Hermes use to reach Yasin-Operations once that integration is implemented?
- What health-check contract will Yasin-Operations expose to other ecosystem projects, if any?
- Should Yasin-Operations be added to the ecosystem's cross-repository E2E certification once it has real integration surface area?
