"""Unit tests for the contract-boundary scanner (YASIN-DOCS #10)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures"
GOOD = FIXTURES / "good"
BAD = FIXTURES / "bad"

# Ensure package is importable when tests run from repo root
sys.path.insert(0, str(ROOT.parents[1]))

from tools.contract_boundary.scanner import (  # noqa: E402
    FORBIDDEN_TOP_LEVEL,
    PUBLIC_PREFIXES,
    scan_file,
    scan_tree,
)


def test_public_only_passes():
    v = scan_file(GOOD / "public_only.py")
    assert v == [], [x.format() for x in v]


def test_no_ai_passes():
    v = scan_file(GOOD / "no_ai.py")
    assert v == []


def test_comments_do_not_false_positive():
    """Comments and docstrings mentioning forbidden names must not fail."""
    v = scan_file(GOOD / "public_only.py")
    assert not any("knowledge_platform" in x.name for x in v)
    assert not any("security_platform" in x.name for x in v)


def test_private_top_level_fails():
    v = scan_file(BAD / "private_top_level.py")
    assert len(v) >= 3
    names = {x.name.split(".")[0] for x in v}
    assert "knowledge_platform" in names
    assert "security_platform" in names
    assert "developer_platform" in names


def test_private_yasinai_sub_fails():
    v = scan_file(BAD / "private_yasinai_sub.py")
    assert len(v) >= 2
    assert any("yasinai.core" in x.name or "core" in x.reason for x in v)


def test_scan_tree_good_ok():
    v = scan_tree(GOOD)
    assert v == []


def test_scan_tree_bad_fails():
    v = scan_tree(BAD)
    assert len(v) >= 4


def test_cli_exit_codes():
    proc_ok = subprocess.run(
        [sys.executable, "-m", "tools.contract_boundary", str(GOOD)],
        cwd=str(ROOT.parents[1]),
        capture_output=True,
        text=True,
    )
    assert proc_ok.returncode == 0, proc_ok.stdout + proc_ok.stderr

    proc_bad = subprocess.run(
        [sys.executable, "-m", "tools.contract_boundary", str(BAD)],
        cwd=str(ROOT.parents[1]),
        capture_output=True,
        text=True,
    )
    assert proc_bad.returncode == 1, proc_bad.stdout + proc_bad.stderr


def test_public_prefixes_documented():
    assert "yasinai.contracts" in PUBLIC_PREFIXES
    assert "yasinai.services" in PUBLIC_PREFIXES
    assert "yasinai.providers" in PUBLIC_PREFIXES


def test_forbidden_top_level_set():
    assert FORBIDDEN_TOP_LEVEL == frozenset(
        {"knowledge_platform", "security_platform", "developer_platform"}
    )


def test_line_numbers_reported():
    v = scan_file(BAD / "private_top_level.py")
    assert all(x.lineno >= 1 for x in v)
    assert all(x.col >= 1 for x in v)
