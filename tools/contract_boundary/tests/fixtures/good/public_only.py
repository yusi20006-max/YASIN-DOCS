"""Allowed public-only imports (must PASS the scanner)."""

from yasinai.contracts import GenerationRequest
from yasinai.services import GenerationService
import yasinai.providers  # noqa: F401

# Mention of forbidden names in comments must not false-positive:
# knowledge_platform security_platform developer_platform yasinai.core

def example():
    """Docstring may mention knowledge_platform without counting as import."""
    s = "security_platform is private"
    return s
