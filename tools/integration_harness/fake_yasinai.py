"""
Offline fake of Yasin-AI public contracts for cross-repo integration tests
(YASIN-DOCS #11).

Mirrors the public surface only:
  - GenerationRequest
  - GenerationResponse / success text
  - GenerationService.generate(...)
No network, no real providers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class GenerationRequest:
    prompt: str
    model: Optional[str] = None
    max_tokens: int = 1024
    temperature: float = 0.7
    system_prompt: Optional[str] = None
    provider: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GenerationResponse:
    text: str
    model: Optional[str] = None
    provider: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    raw: Optional[Any] = None


class GenerationError(Exception):
    """Raised by FakeGenerationService when configured to fail."""


class FakeGenerationService:
    """
    Injectable GenerationService stand-in.

    Configure behaviour via constructor:
      fail: if True, generate() raises GenerationError
      empty: if True, returns empty text
      fixed_text: override response text
    """

    def __init__(
        self,
        *,
        fail: bool = False,
        empty: bool = False,
        fixed_text: str = "processed-content",
        echo_request: bool = False,
    ) -> None:
        self.fail = fail
        self.empty = empty
        self.fixed_text = fixed_text
        self.echo_request = echo_request
        self.last_request: Optional[GenerationRequest] = None
        self.call_count = 0

    def generate(self, request: GenerationRequest) -> GenerationResponse:
        self.call_count += 1
        self.last_request = request
        if self.fail:
            raise GenerationError("fake provider failure")
        text = "" if self.empty else (request.prompt if self.echo_request else self.fixed_text)
        return GenerationResponse(
            text=text,
            model=request.model,
            provider=request.provider or "fake",
            usage={"prompt_tokens": 1, "completion_tokens": 1},
        )
