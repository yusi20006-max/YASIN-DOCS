"""Unit tests for architecture boundary policy (YASIN-DOCS #12)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT.parent))

from tools.architecture_boundary.policy import (  # noqa: E402
    DOMAIN_APPS,
    check_allowed_fixture,
    check_forbidden_fixture,
    check_graph,
)


def test_allowed_graph_clean():
    assert check_allowed_fixture() == []


def test_ai_must_not_depend_on_domain():
    v = check_graph([("Yasin-AI", "YasinRelay")])
    codes = {x.code for x in v}
    assert "AI-OWN-1" in codes


def test_consumer_private_ai_forbidden():
    v = check_graph([("Yasinfeed", "knowledge_platform")])
    codes = {x.code for x in v}
    assert "CONS-1" in codes


def test_consumer_public_ai_allowed():
    v = check_graph([("YasinRelay", "yasinai.contracts")])
    assert v == []


def test_cycle_detected():
    v = check_graph([("A", "B"), ("B", "C"), ("C", "A")])
    codes = {x.code for x in v}
    assert "CYCLE-1" in codes


def test_no_cycle_on_dag():
    v = check_graph([("A", "B"), ("B", "C")])
    assert not any(x.code == "CYCLE-1" for x in v)


def test_forbidden_fixture_fails():
    v = check_forbidden_fixture()
    codes = {x.code for x in v}
    assert {"AI-OWN-1", "CONS-1", "CYCLE-1", "OWN-PIPE-1"}.issubset(codes)


def test_domain_apps_set():
    assert "YasinRelay" in DOMAIN_APPS
    assert "Yasinfeed" in DOMAIN_APPS
