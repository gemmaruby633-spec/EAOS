"""Master Shared Libraries Entrypoint Engine."""

from __future__ import annotations

from libs.core.shared_primitives import ResultDTO
from libs.crypto.security_utils import CryptographicUtils
from libs.validation.schema_validator import SchemaValidatorHelper


class EAOSSharedLibsEngine:
    """Master Engine managing shared utility primitives and crypto."""

    def __init__(self) -> None:
        self.validator = SchemaValidatorHelper()
        self.crypto = CryptographicUtils()

    def compute_payload_evidence(self, payload: str) -> ResultDTO:
        """Compute evidence hash for payload string."""
        digest = self.crypto.calculate_sha256(payload)
        return ResultDTO(
            success=True,
            message="Evidence computed successfully.",
            data={"digest": digest},
        )
