"""Cross-repository E2E certification harness (YASIN-DOCS #15)."""

__all__ = ["run_certification", "CertificationResult"]

from .certify import CertificationResult, run_certification
