from __future__ import annotations

import sys
from pathlib import Path

from .scan_secrets import scan_tree


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    roots = [Path(a) for a in argv] if argv else [Path(".")]
    total = 0
    for root in roots:
        findings = scan_tree(root)
        for f in findings:
            print(f"[SECRET?] {f}")
            total += 1
    if total:
        print(f"\n{total} potential secret pattern(s) found")
        return 1
    print("No high-confidence secret patterns found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
