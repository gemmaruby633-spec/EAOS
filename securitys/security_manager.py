"""Security manager module."""

from __future__ import annotations

from .automation.dry_run_security_simulator import DryRunSecuritySimulator
from .compliance.zero_trust_auditor import ZeroTrustAuditor


class SecurityManager:
    """Security manager."""

    def __init__(self) -> None:
        self.auditor = ZeroTrustAuditor()
        self.simulator = DryRunSecuritySimulator()
