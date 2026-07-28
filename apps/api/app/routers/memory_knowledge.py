"""Knowledge, Capability, Memory and Intelligence router."""

from typing import Any
from fastapi import APIRouter
from packages.capability.domain.models import BusinessCapability
from packages.capability.infrastructure.adapters import InMemoryCapabilityRegistry
from packages.knowledge.application.use_cases import StoreKnowledgeRequest, StoreKnowledgeUseCase
from packages.knowledge.domain.models import KnowledgeArtifact
from packages.knowledge.infrastructure.adapters import SplayCacheKnowledgeRepository
from packages.memory.domain.entities import MemoryRecord
from packages.memory.infrastructure.repository import InMemoryMemoryRepository

router = APIRouter(tags=["Memory & Knowledge"])
capability_registry = InMemoryCapabilityRegistry()
knowledge_repo = SplayCacheKnowledgeRepository(None)
memory_repo = InMemoryMemoryRepository()


@router.post("/knowledge", response_model=KnowledgeArtifact, status_code=201)
async def create_knowledge(request: StoreKnowledgeRequest) -> KnowledgeArtifact:
    use_case = StoreKnowledgeUseCase(knowledge_repo)
    return use_case.execute(request)


@router.get("/v1/capabilities", response_model=list[BusinessCapability])
async def v1_list_capabilities() -> list[BusinessCapability]:
    return capability_registry.list_all()


@router.get("/v1/memory", response_model=list[MemoryRecord])
async def v1_list_memories() -> list[MemoryRecord]:
    return memory_repo.list_all()


@router.post("/v1/memory/store", status_code=201)
def store_memory(req: dict[str, Any]) -> dict[str, Any]:
    return {"status": "STORED", "memory_id": "MEM-01"}


@router.post("/memory/hybrid-search")
async def hybrid_memory_search(request: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    return [{"id": "res_1", "score": 0.98}]


@router.post("/intelligence/drift/evaluate")
async def evaluate_model_drift(request: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"hallucination_detected": True, "recommended_action": "FALLBACK_MODEL"}


@router.post("/intelligence/models/route")
async def route_intelligence_model(request: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"selected_model": "ollama/llama3"}
