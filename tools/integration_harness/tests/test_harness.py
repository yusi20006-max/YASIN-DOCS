"""Offline integration harness tests (YASIN-DOCS #11)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT.parent))

from tools.integration_harness.consumer_adapters import (  # noqa: E402
    feed_rewrite,
    press_ai,
    relay_process,
)
from tools.integration_harness.fake_yasinai import (  # noqa: E402
    FakeGenerationService,
    GenerationError,
    GenerationRequest,
)


def test_request_contract_fields_preserved():
    svc = FakeGenerationService(fixed_text="out")
    req = GenerationRequest(
        prompt="hello",
        model="gpt-test",
        max_tokens=50,
        temperature=0.2,
        system_prompt="sys",
        provider="openai",
        metadata={"src": "test"},
    )
    resp = svc.generate(req)
    assert svc.last_request is req
    assert svc.last_request.model == "gpt-test"
    assert svc.last_request.provider == "openai"
    assert resp.model == "gpt-test"
    assert resp.provider == "openai"


def test_response_contract_success():
    svc = FakeGenerationService(fixed_text="rewritten")
    resp = svc.generate(GenerationRequest(prompt="in"))
    assert resp.text == "rewritten"
    assert resp.usage is not None


def test_error_contract_raises():
    svc = FakeGenerationService(fail=True)
    try:
        svc.generate(GenerationRequest(prompt="x"))
        assert False, "expected GenerationError"
    except GenerationError:
        pass


def test_model_provider_preservation_on_request():
    svc = FakeGenerationService()
    relay_process(svc, "t", model="m1", provider="p1")
    assert svc.last_request is not None
    assert svc.last_request.model == "m1"
    assert svc.last_request.provider == "p1"


def test_relay_passthrough_on_failure():
    svc = FakeGenerationService(fail=True)
    out = relay_process(svc, "original")
    assert out == "original"


def test_relay_success():
    svc = FakeGenerationService(fixed_text="ok")
    assert relay_process(svc, "original") == "ok"


def test_feed_raises_on_failure():
    svc = FakeGenerationService(fail=True)
    try:
        feed_rewrite(svc, "x")
        assert False, "expected GenerationError"
    except GenerationError:
        pass


def test_feed_success():
    svc = FakeGenerationService(fixed_text="rewritten")
    assert feed_rewrite(svc, "x") == "rewritten"


def test_press_result_failure():
    svc = FakeGenerationService(fail=True)
    r = press_ai(svc, "x")
    assert r.ok is False
    assert r.error


def test_press_result_success():
    svc = FakeGenerationService(fixed_text="press-ok")
    r = press_ai(svc, "x")
    assert r.ok is True
    assert r.text == "press-ok"


def test_provider_fallback_empty_text_relay():
    svc = FakeGenerationService(empty=True)
    assert relay_process(svc, "orig") == "orig"


def test_no_network_required():
    """Harness must not attempt any network I/O."""
    svc = FakeGenerationService()
    assert relay_process(svc, "a") == "processed-content"
    assert feed_rewrite(svc, "b") == "processed-content"
    assert press_ai(svc, "c").ok is True
