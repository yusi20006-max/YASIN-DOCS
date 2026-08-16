"""Tests for cross-repo E2E certification harness (#15)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT.parent))

from tools.e2e_certification.certify import (  # noqa: E402
    PUBLIC_CONTRACT_VERSION,
    run_certification,
)


def test_all_certification_checks_pass():
    results = run_certification()
    failed = [r for r in results if not r.ok]
    assert not failed, f"failures: {[(r.repository, r.check, r.detail) for r in failed]}"
    assert len(results) >= 9


def test_repositories_are_identified():
    results = run_certification()
    repos = {r.repository for r in results}
    assert "YasinRelay" in repos
    assert "Yasinfeed" in repos
    assert "YasinPress-Rewrite-" in repos
    assert "Yasin-AI-contracts" in repos


def test_contract_version_declared():
    assert PUBLIC_CONTRACT_VERSION == "1.1.4"


def test_cli_exit_zero():
    from tools.e2e_certification.__main__ import main

    assert main([]) == 0
