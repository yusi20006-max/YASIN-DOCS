"""Forbidden top-level private packages — must FAIL the scanner."""

import knowledge_platform
from security_platform.auth import something
import developer_platform.sdk
