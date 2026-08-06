"""Federation manager."""

from __future__ import annotations

from .bft.synod_bft import SynodBft


class FederationManager:
    """Federation manager."""

    def __init__(self) -> None:
        self.bft = SynodBft()
