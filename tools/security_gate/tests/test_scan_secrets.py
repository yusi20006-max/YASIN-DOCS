from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT.parent))

from tools.security_gate.scan_secrets import scan_tree  # noqa: E402


def test_clean_tree_has_no_secrets(tmp_path: Path):
    (tmp_path / "ok.py").write_text("API_KEY = os.environ.get('API_KEY')\n")
    assert scan_tree(tmp_path) == []


def test_detects_private_key(tmp_path: Path):
    header = "-----BEGIN " + "RSA PRIVATE KEY-----"
    (tmp_path / "key.txt").write_text(header + "\nMIIE\n")
    hits = scan_tree(tmp_path)
    assert any("private_key_block" in h for h in hits)


def test_docs_repo_self_scan():
    docs_root = Path(__file__).resolve().parents[3]
    findings = scan_tree(docs_root)
    findings = [f for f in findings if "/tools/security_gate/tests/" not in f]
    assert findings == [], findings
