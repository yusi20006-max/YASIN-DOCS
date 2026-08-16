"""Mock cross-repo integration harness (YASIN-DOCS #11)."""

from .fake_yasinai import (
    FakeGenerationService,
    GenerationError,
    GenerationRequest,
    GenerationResponse,
)
from .consumer_adapters import PressAIResult, feed_rewrite, press_ai, relay_process

__all__ = [
    "FakeGenerationService",
    "GenerationError",
    "GenerationRequest",
    "GenerationResponse",
    "PressAIResult",
    "feed_rewrite",
    "press_ai",
    "relay_process",
]
