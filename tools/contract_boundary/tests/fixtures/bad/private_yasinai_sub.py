"""Forbidden private yasinai submodules — must FAIL the scanner."""

from yasinai.core import runtime
import yasinai.private_modules
from yasinai.cli.security_entrypoint import main
