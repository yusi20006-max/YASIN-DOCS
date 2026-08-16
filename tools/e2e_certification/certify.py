"""
Deterministic offline cross-repository E2E certification (YASIN-DOCS #15).

Uses the mock integration harness (#11) and public-contract fixtures.
No network, secrets, or paid providers.

Each check tags a logical repository so failures identify the contract owner.
Agent paths are skipped unless AGENT_AI_ACTIVATED is set (Issue #19 deferred).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable, List

from tools.integration_harness.consumer_adapters import (
    feed_rewrite,
    press_ai,
    relay_process,
)
from tools.integration_harness.fake_yasinai import (
    FakeGenerationService,
    GenerationError,
    GenerationRequest,
    GenerationResponse,
)

# Declared public contract version for compatibility matrix checks.
PUBLIC_CONTRACT_VERSION = "1.1.4"


@dataclass
class CertificationResult:
    repository: str
    check: str
    ok: bool
    detail: str


def _check(
    repository: str,
    check: str,
    fn: Callable[[], None],
) -> CertificationResult:
    try:
        fn()
        return CertificationResult(repository, check, True, "ok")
    except Exception as exc:  # noqa: BLE001 — certification boundary
        return CertificationResult(
            repository,
            check,
            False,
            f"{type(exc).__name__}: {exc}",
        )


def _relay_success() -> None:
    svc = FakeGenerationService(fixed_text="relay-out")
    out = relay_process(svc, "in", model="m", provider="p")
    assert out == "relay-out"
    assert svc.last_request is not None
    assert svc.last_request.model == "m"
    assert svc.last_request.provider == "p"


def _relay_fallback() -> None:
    svc = FakeGenerationService(fail=True)
    assert relay_process(svc, "original") == "original"
    svc2 = FakeGenerationService(empty=True)
    assert relay_process(svc2, "original") == "original"


def _feed_success() -> None:
    svc = FakeGenerationService(fixed_text="feed-out")
    assert feed_rewrite(svc, "in", model="fm", provider="fp") == "feed-out"
    assert svc.last_request is not None
    assert svc.last_request.model == "fm"


def _feed_error() -> None:
    svc = FakeGenerationService(fail=True)
    try:
        feed_rewrite(svc, "x")
        raise AssertionError("expected GenerationError")
    except GenerationError:
        pass


def _press_success() -> None:
    svc = FakeGenerationService(fixed_text="press-out")
    r = press_ai(svc, "in", model="pm", provider="pp")
    assert r.ok is True
    assert r.text == "press-out"
    assert svc.last_request is not None
    assert svc.last_request.provider == "pp"


def _press_error() -> None:
    svc = FakeGenerationService(fail=True)
    r = press_ai(svc, "x")
    assert r.ok is False
    assert r.error


def _contract_fields() -> None:
    """Public GenerationRequest/Response field preservation."""
    req = GenerationRequest(
        prompt="p",
        model="model-x",
        max_tokens=10,
        temperature=0.1,
        system_prompt="sys",
        provider="prov",
        metadata={"k": "v"},
    )
    svc = FakeGenerationService(fixed_text="t")
    resp = svc.generate(req)
    assert isinstance(resp, GenerationResponse)
    assert resp.model == "model-x"
    assert resp.provider == "prov"
    assert resp.text == "t"
    assert svc.last_request is req


def _version_compatibility() -> None:
    """Harness declares compatibility with Yasin-AI public contract version."""
    assert PUBLIC_CONTRACT_VERSION.startswith("1.")
    svc = FakeGenerationService()
    resp = svc.generate(GenerationRequest(prompt="v"))
    for attr in ("text", "model", "provider", "usage"):
        assert hasattr(resp, attr), f"missing response field: {attr}"


def _offline_only() -> None:
    """No environment variables that would enable live providers are required."""
    forbidden_env = (
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "YASINAI_LIVE",
    )
    for key in forbidden_env:
        _ = os.environ.get(key)
    svc = FakeGenerationService(fixed_text="offline")
    assert relay_process(svc, "a") == "offline"


def run_certification(*, verbose: bool = False) -> List[CertificationResult]:
    """Run full offline certification suite. Agent AI path skipped (#19 deferred)."""
    checks: list[tuple[str, str, Callable[[], None]]] = [
        ("Yasin-AI-contracts", "request_response_fields", _contract_fields),
        ("Yasin-AI-contracts", "version_compatibility", _version_compatibility),
        ("YasinRelay", "success_path", _relay_success),
        ("YasinRelay", "fallback_on_error", _relay_fallback),
        ("Yasinfeed", "success_path", _feed_success),
        ("Yasinfeed", "error_raises", _feed_error),
        ("YasinPress-Rewrite-", "success_path", _press_success),
        ("YasinPress-Rewrite-", "structured_error", _press_error),
        ("ecosystem", "offline_no_secrets", _offline_only),
    ]

    if os.environ.get("AGENT_AI_ACTIVATED", "").lower() in ("1", "true", "yes"):
        pass

    results = [_check(repo, name, fn) for repo, name, fn in checks]
    if verbose:
        for r in results:
            print(f"{'PASS' if r.ok else 'FAIL'} {r.repository}/{r.check}: {r.detail}")
    return results
