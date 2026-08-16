"""
Minimal consumer adapter patterns matching Relay / Feed / Press semantics
(YASIN-DOCS #11).

These are harness stand-ins, not production code. They encode the documented
failure contracts:
  - Relay: passthrough original text on AI failure
  - Feed: raise on AI failure
  - Press: structured failure result (no raise)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .fake_yasinai import (
    FakeGenerationService,
    GenerationError,
    GenerationRequest,
)


@dataclass
class PressAIResult:
    ok: bool
    text: str = ""
    error: Optional[str] = None


def relay_process(
    service: FakeGenerationService,
    text: str,
    *,
    model: Optional[str] = None,
    provider: Optional[str] = None,
) -> str:
    """Relay pattern: on failure return original text (passthrough)."""
    req = GenerationRequest(prompt=text, model=model, provider=provider)
    try:
        resp = service.generate(req)
        if not resp.text:
            return text  # empty → passthrough
        return resp.text
    except GenerationError:
        return text


def feed_rewrite(
    service: FakeGenerationService,
    text: str,
    *,
    model: Optional[str] = None,
    provider: Optional[str] = None,
) -> str:
    """Feed pattern: on failure raise (caller decides)."""
    req = GenerationRequest(prompt=text, model=model, provider=provider)
    resp = service.generate(req)  # may raise
    if not resp.text:
        raise GenerationError("empty rewrite")
    return resp.text


def press_ai(
    service: FakeGenerationService,
    text: str,
    *,
    model: Optional[str] = None,
    provider: Optional[str] = None,
) -> PressAIResult:
    """Press pattern: structured result, never raises for provider errors."""
    req = GenerationRequest(prompt=text, model=model, provider=provider)
    try:
        resp = service.generate(req)
        if not resp.text:
            return PressAIResult(ok=False, error="empty response")
        return PressAIResult(ok=True, text=resp.text)
    except GenerationError as e:
        return PressAIResult(ok=False, error=str(e))
