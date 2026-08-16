"""
Architecture boundary policy checks for the Yasin ecosystem (YASIN-DOCS #12).

Encodes ownership and dependency-direction rules without requiring a full
multi-repo checkout. Rules are evaluated against declared dependency graphs
(fixtures or caller-supplied edges).

Rules:
  AI-OWN-1   Yasin-AI must not depend on domain apps
  CONS-1     Consumers must not depend on private Yasin-AI modules
  CYCLE-1    Circular dependency among canonical packages is detected
  OWN-PIPE-1 Domain pipeline orchestration stays in domain apps (not Yasin-AI)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Set, Tuple

DOMAIN_APPS: frozenset[str] = frozenset(
    {
        "YasinRelay",
        "Yasinfeed",
        "YasinPress",
        "YasinPress-Rewrite-",
        "Yasin-agent",
        "YasinHub",
        "Yasin-cli",
        "Yasin-Agent",
        "YasinCLI",
    }
)

AI_PACKAGES: frozenset[str] = frozenset(
    {
        "Yasin-AI",
        "yasinai",
        "knowledge_platform",
        "security_platform",
        "developer_platform",
    }
)

PRIVATE_AI_MODULES: frozenset[str] = frozenset(
    {
        "knowledge_platform",
        "security_platform",
        "developer_platform",
        "yasinai.core",
        "yasinai.cli",
        "yasinai.private_modules",
    }
)

# Canonical allowed edges (consumer → public AI only). Used as the clean fixture.
ALLOWED_GRAPH: Dict[str, Set[str]] = {
    "YasinRelay": {"yasinai.contracts", "yasinai.services", "yasinai.providers"},
    "Yasinfeed": {"yasinai.contracts", "yasinai.services", "yasinai.providers"},
    "YasinPress": {"yasinai.contracts", "yasinai.services"},
    "Yasin-AI": set(),  # AI does not depend on domain apps
    "yasinai": set(),
}


@dataclass(frozen=True)
class PolicyViolation:
    code: str
    message: str

    def format(self) -> str:
        return f"[{self.code}] {self.message}"


Edge = Tuple[str, str]  # (from_pkg, to_pkg)


def _detect_cycles(edges: Sequence[Edge]) -> List[List[str]]:
    """Simple DFS cycle detection; returns list of cycles (as node lists)."""
    graph: Dict[str, Set[str]] = {}
    for a, b in edges:
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set())

    cycles: List[List[str]] = []
    visited: Set[str] = set()
    stack: List[str] = []
    on_stack: Set[str] = set()

    def dfs(node: str) -> None:
        visited.add(node)
        stack.append(node)
        on_stack.add(node)
        for nbr in graph.get(node, ()):
            if nbr not in visited:
                dfs(nbr)
            elif nbr in on_stack:
                # extract cycle
                if nbr in stack:
                    i = stack.index(nbr)
                    cycles.append(stack[i:] + [nbr])
        stack.pop()
        on_stack.discard(node)

    for n in list(graph):
        if n not in visited:
            dfs(n)
    return cycles


def check_graph(edges: Sequence[Edge]) -> List[PolicyViolation]:
    """Evaluate all architecture rules against a declared edge list."""
    violations: List[PolicyViolation] = []

    for src, dst in edges:
        # AI-OWN-1
        if src in AI_PACKAGES or src.startswith("yasinai"):
            if dst in DOMAIN_APPS or any(dst.startswith(d) for d in DOMAIN_APPS):
                violations.append(
                    PolicyViolation(
                        "AI-OWN-1",
                        f"Yasin-AI (or its packages) must not depend on domain apps ({src} → {dst})",
                    )
                )
            # OWN-PIPE-1: AI must not own domain pipeline orchestration
            if dst in DOMAIN_APPS:
                violations.append(
                    PolicyViolation(
                        "OWN-PIPE-1",
                        f"AI ownership boundary: domain pipeline orchestration must stay in domain apps ({src} → {dst})",
                    )
                )

        # CONS-1
        if src in DOMAIN_APPS or any(src.startswith(d) for d in DOMAIN_APPS):
            if dst in PRIVATE_AI_MODULES or any(
                dst == p or dst.startswith(p + ".") for p in PRIVATE_AI_MODULES
            ):
                violations.append(
                    PolicyViolation(
                        "CONS-1",
                        f"Consumer must not depend on private Yasin-AI module ({src} → {dst})",
                    )
                )

    # CYCLE-1
    for cycle in _detect_cycles(edges):
        if len(cycle) >= 2:
            path = " → ".join(cycle)
            violations.append(
                PolicyViolation("CYCLE-1", f"Circular dependency detected: {path}")
            )

    return violations


def check_allowed_fixture() -> List[PolicyViolation]:
    """Canonical allowed graph must produce zero violations."""
    edges: List[Edge] = []
    for src, dests in ALLOWED_GRAPH.items():
        for d in dests:
            edges.append((src, d))
    return check_graph(edges)


def check_forbidden_fixture() -> List[PolicyViolation]:
    """A deliberately bad graph must produce the expected rule codes."""
    bad_edges: List[Edge] = [
        ("Yasin-AI", "YasinRelay"),  # AI-OWN-1 + OWN-PIPE-1
        ("Yasinfeed", "knowledge_platform"),  # CONS-1
        ("A", "B"),
        ("B", "C"),
        ("C", "A"),  # CYCLE-1
    ]
    return check_graph(bad_edges)


def main() -> int:
    import sys

    print("=== Architecture boundary policy ===")
    clean = check_allowed_fixture()
    if clean:
        print("FAIL: allowed graph produced violations:")
        for v in clean:
            print(" ", v.format())
        return 1
    print("PASS: canonical allowed graph — no violations")

    bad = check_forbidden_fixture()
    if not bad:
        print("FAIL: forbidden fixture produced zero violations")
        return 1
    codes = {v.code for v in bad}
    expected = {"AI-OWN-1", "CONS-1", "CYCLE-1", "OWN-PIPE-1"}
    if not expected.issubset(codes):
        print(f"FAIL: missing expected codes. got={codes} expected⊆{expected}")
        return 1
    print(f"PASS: forbidden fixture correctly reported {len(bad)} violation(s):")
    for v in bad:
        print(" ", v.format())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
