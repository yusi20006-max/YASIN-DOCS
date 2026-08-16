"""CLI: python -m tools.e2e_certification"""

from __future__ import annotations

import sys

from .certify import run_certification


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    verbose = "--verbose" in argv or "-v" in argv
    results = run_certification(verbose=verbose)
    failed = [r for r in results if not r.ok]
    for r in results:
        status = "PASS" if r.ok else "FAIL"
        print(f"[{status}] {r.repository}: {r.check} — {r.detail}")
    if failed:
        print(f"\n{len(failed)} failure(s) of {len(results)} checks")
        return 1
    print(f"\nAll {len(results)} certification checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
