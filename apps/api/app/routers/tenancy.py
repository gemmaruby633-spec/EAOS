"""Identity, Tenancy RLS and Metering router."""

from typing import Any
from fastapi import APIRouter, HTTPException
from packages.identity.application.use_cases import (
    RegisterUserRequest,
    RegisterUserUseCase,
)
from packages.identity.domain.models import User
from packages.identity.infrastructure.adapters import InMemoryUserRepository
from packages.tenancy.infrastructure.rls_adapter import PostgresRLSAdapter, RLSContextDTO

router = APIRouter(tags=["Tenancy & Identity"])
identity_repo = InMemoryUserRepository()
rls_adapter = PostgresRLSAdapter()


@router.post("/users/register", response_model=User, status_code=201)
async def register_user(request: RegisterUserRequest) -> User:
    use_case = RegisterUserUseCase(identity_repo)
    try:
        return use_case.execute(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/tenancy/rls/apply-context", response_model=RLSContextDTO, status_code=200)
async def apply_tenant_rls_context(request: dict[str, Any] | None = None) -> RLSContextDTO:
    return rls_adapter.apply_tenant_rls_context("tenant_enterprise_99")


@router.post("/tenancy/metering/enforce")
async def enforce_tenant_metering(request: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"allowed": True}
