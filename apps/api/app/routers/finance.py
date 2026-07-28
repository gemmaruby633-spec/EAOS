"""FastAPI Router for Finance Capability Application."""

from typing import Any

from fastapi import APIRouter
from packages.finance.application.use_cases import (
    RecordFinancialTransactionUseCase,
)
from pydantic import BaseModel, ConfigDict

router = APIRouter(prefix="/v1/finance", tags=["Finance Capability"])


class FinancialTxRequest(BaseModel):
    """Value object representing financial ledger transaction payload."""

    model_config = ConfigDict(frozen=True)

    revenue_usd: float = 0.0
    cost_usd: float = 0.0
    entry_type: str = "AFFILIATE_PAYOUT"


@router.post("/ledger/record")
async def record_transaction(
    request: FinancialTxRequest,
) -> dict[str, Any]:
    """Records transaction into financial ledger."""
    use_case = RecordFinancialTransactionUseCase()
    entry = use_case.execute(request.revenue_usd, request.cost_usd, request.entry_type)
    return entry.model_dump()
