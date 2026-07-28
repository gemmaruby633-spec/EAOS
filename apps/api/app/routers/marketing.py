"""FastAPI Router for Marketing Capability Package."""

from typing import Any

from fastapi import APIRouter
from packages.marketing.application.use_cases import (
    ExecuteKeywordResearchUseCase,
)
from pydantic import BaseModel, ConfigDict

router = APIRouter(prefix="/v1/marketing", tags=["Marketing Capability"])


class KeywordResearchRequest(BaseModel):
    """Value object representing keyword research request."""

    model_config = ConfigDict(frozen=True)

    keyword: str


@router.post("/keywords/research")
async def research_keyword(
    request: KeywordResearchRequest,
) -> dict[str, Any]:
    """Executes keyword research workflow."""
    use_case = ExecuteKeywordResearchUseCase()
    target = use_case.execute(request.keyword)
    return target.model_dump()
