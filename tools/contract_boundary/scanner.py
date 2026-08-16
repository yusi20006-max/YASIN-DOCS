"""
Cross-repository public-contract boundary scanner for Yasin ecosystem.

Scans Python source trees for imports of private Yasin-AI implementation
modules. Consumers must use only public surfaces:
  - yasinai
  - yasinai.contracts
  - yasinai.services
  - yasinai.providers
  (and documented public submodules under those packages)

Forbidden:
  - knowledge_platform
  - security_platform
  - developer_platform
  - any other non-public yasinai.* implementation package

Comments, docstrings, and string literals do not count as imports.
"""

from __future__ import annotations

import ast
import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Set

PUBLIC_PREFIXES: tuple[str, ...] = (
    "yasinai",
    "yasinai.contracts",
    "yasinai.services",
    "yasinai.providers",
)

FORBIDDEN_TOP_LEVEL: frozenset[str] = frozenset(
    {
        "knowledge_platform",
        "security_platform",
        "developer_platform",
    }
)

# Private yasinai subpackages (anything under yasinai that is not public)
PRIVATE_YASINAI_PREFIXES: tuple[str, ...] = (
    "yasinai.core",
    "yasinai.cli",
    "yasinai.deployment",
    "yasinai.integration",
    "yasinai.private_modules",
    "yasinai.compatibility",
)


@dataclass(frozen=True)
class Violation:
    path: str
    lineno: int
    col: int
    name: str
    reason: str

    def format(self) -> str:
        return f"{self.path}:{self.lineno}:{self.col}: forbidden import '{self.name}' ({self.reason})"


def _is_public(name: str) -> bool:
    """Return True if the dotted import name is an allowed public surface."""
    if name in PUBLIC_PREFIXES:
        return True
    for prefix in PUBLIC_PREFIXES:
        if name.startswith(prefix + "."):
            # Still public only if it stays under the public root
            # (e.g. yasinai.contracts.foo is ok; yasinai.core.foo is not)
            rest = name[len(prefix) + 1 :]
            if prefix == "yasinai":
                # top-level yasinai is allowed; submodules must match known public
                first = rest.split(".", 1)[0]
                if first in ("contracts", "services", "providers"):
                    return True
                return False
            return True
    return False


def _classify(name: str) -> Optional[str]:
    """
    Return a reason string if the import is forbidden, else None.
    """
    top = name.split(".", 1)[0]
    if top in FORBIDDEN_TOP_LEVEL:
        return f"private top-level package '{top}'"
    if top == "yasinai" and not _is_public(name):
        return f"private yasinai implementation '{name.split('.', 2)[0] if name.count('.') >= 1 else name}'"
    for priv in PRIVATE_YASINAI_PREFIXES:
        if name == priv or name.startswith(priv + "."):
            return f"private yasinai implementation '{priv}'"
    return None


class _ImportVisitor(ast.NodeVisitor):
    def __init__(self, path: str) -> None:
        self.path = path
        self.violations: List[Violation] = []

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            reason = _classify(alias.name)
            if reason:
                self.violations.append(
                    Violation(self.path, node.lineno, node.col_offset + 1, alias.name, reason)
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module is None:
            self.generic_visit(node)
            return
        # from X import a, b  → check X and X.a, X.b
        base = node.module
        reason = _classify(base)
        if reason:
            self.violations.append(
                Violation(self.path, node.lineno, node.col_offset + 1, base, reason)
            )
        else:
            for alias in node.names:
                if alias.name == "*":
                    continue
                full = f"{base}.{alias.name}"
                reason2 = _classify(full)
                if reason2:
                    self.violations.append(
                        Violation(self.path, node.lineno, node.col_offset + 1, full, reason2)
                    )
        self.generic_visit(node)


def scan_file(path: Path) -> List[Violation]:
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError:
        return []
    visitor = _ImportVisitor(str(path))
    visitor.visit(tree)
    return visitor.violations


def scan_tree(
    root: Path,
    *,
    exclude_dirs: Optional[Set[str]] = None,
) -> List[Violation]:
    exclude = exclude_dirs or {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".pytest_cache",
        "node_modules",
        ".tox",
        "dist",
        "build",
        ".mypy_cache",
        ".ruff_cache",
    }
    violations: List[Violation] = []
    if not root.exists():
        return violations
    for py in sorted(root.rglob("*.py")):
        # skip excluded path segments
        if any(part in exclude for part in py.parts):
            continue
        violations.extend(scan_file(py))
    return violations


def format_report(root: Path, violations: Sequence[Violation]) -> str:
    files = list(root.rglob("*.py")) if root.exists() else []
    n_files = len([p for p in files if not any(x in p.parts for x in (".git", "__pycache__", ".venv"))])
    lines: List[str] = []
    if not violations:
        lines.append(f"=== PASS: {root} ({n_files} files) ===")
        lines.append("  No private-import violations.")
        lines.append("")
        lines.append("Summary: ALL PASS")
    else:
        lines.append(f"=== FAIL: {root} ({n_files} files) ===")
        for v in violations:
            lines.append(f"  {v.format()}")
        lines.append("")
        lines.append(f"Summary: FAILED with {len(violations)} violation(s)")
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Scan Python trees for private Yasin-AI / platform imports."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="One or more roots to scan",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print summary lines",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    any_fail = False
    for root in args.paths:
        root = root.resolve()
        viols = scan_tree(root)
        report = format_report(root, viols)
        if not args.quiet or viols:
            print(report)
            print()
        if viols:
            any_fail = True
    if any_fail:
        print("Summary: FAILED") if args.quiet else None
        return 1
    if args.quiet:
        print("Summary: ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
