"""Contract boundary scanner package (YASIN-DOCS #10)."""

from .scanner import (
    FORBIDDEN_TOP_LEVEL,
    PUBLIC_PREFIXES,
    Violation,
    scan_file,
    scan_tree,
)

__all__ = [
    "FORBIDDEN_TOP_LEVEL",
    "PUBLIC_PREFIXES",
    "Violation",
    "scan_file",
    "scan_tree",
]
