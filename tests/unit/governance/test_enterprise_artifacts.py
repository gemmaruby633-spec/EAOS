"""Unit test suite verifying integrity of Enterprise Artifacts."""

from pathlib import Path

from packages.frameworks.application.ai_enterprise_architect import (
    AIEnterpriseArchitectEngine,
)
from packages.frameworks.application.architecture_validator import (
    ExecutableArchitectureValidator,
)
from packages.frameworks.domain.framework_registry import (
    FrameworkRegistry,
)
from packages.governance.application.use_cases import (
    EvaluateGovernanceUseCase,
)
from packages.governance.domain.models import (
    ArchitecturalMaturityLevel,
    ConstitutionalRule,
    ConstitutionAmendment,
)
from packages.intelligence.infrastructure.zero_cost_router import (
    ZeroCostModelRouter,
)
from packages.legal_governance.application.use_cases import (
    ConductArchitecturalTrialUseCase,
)
from packages.monetization.application.use_cases import (
    BillTenantUsageUseCase,
)
from packages.platform.infrastructure.airgapped_adapter import (
    AirGappedDeploymentEngine,
    AirGappedDeploymentProfileDTO,
    DeploymentTierEnum,
)
from packages.platform.infrastructure.ecosystem_adapter import (
    EcosystemIntegrationEngine,
)
from packages.platform.infrastructure.environment_adapter import (
    AdaptiveEnvironmentEngine,
    ExecutionModeEnum,
)
from packages.self_hosting.application.agency_orchestrator import (
    SolopreneurAgencyOrchestrator,
)
from packages.self_hosting.application.disaster_recovery import (
    ZeroServerDisasterRecoveryEngine,
)
from packages.swarm_intelligence.application.use_cases import (
    OrchestrateSwarmTaskUseCase,
)
from packages.swarm_intelligence.domain.models import InsectRoleEnum
from sdk.embedded_engine import EAOSEmbeddedEngine
from sdk.single_file_engine import EAOSSingleFileEngine


def test_governance_use_case_execution() -> None:
    """Verifies constitutional governance evaluation logic."""
    rule = ConstitutionalRule(
        rule_id="R01",
        title="Hexagonal Boundary",
        statement="Domain layer must remain clean",
    )
    amendment = ConstitutionAmendment(
        amendment_id="AMD-01",
        target_rule="R01",
        proposed_text="Strict typing mandated across domain",
        reasoning="Type safety enforcement",
    )
    uc = EvaluateGovernanceUseCase()
    assert uc.execute(rule, amendment) is True


def test_architectural_maturity_levels() -> None:
    """Verifies 5-tier Architectural Maturity Level enumeration."""
    assert ArchitecturalMaturityLevel.LEVEL_1_STATIC.value == "STATIC"
    assert ArchitecturalMaturityLevel.LEVEL_2_EXECUTABLE.value == "EXECUTABLE"
    assert ArchitecturalMaturityLevel.LEVEL_3_OBSERVABLE.value == "OBSERVABLE"
    assert ArchitecturalMaturityLevel.LEVEL_4_ADAPTIVE.value == "ADAPTIVE"
    assert ArchitecturalMaturityLevel.LEVEL_5_EVOLUTIONARY.value == "EVOLUTIONARY"


def test_sprints_3_to_7_all_in_one_execution() -> None:
    """Verifies Sprints 3-7 Executable Platform Subsystems."""
    reg = FrameworkRegistry.create_default()
    assert len(reg.list()) >= 4

    validator = ExecutableArchitectureValidator()
    report = validator.validate_repository()
    assert report.is_compliant is True

    ai_arch = AIEnterpriseArchitectEngine()
    prop = ai_arch.generate_design_proposal("CRM")
    assert prop.confidence >= 0.95


def test_phases_1_to_6_solopreneur_agency_orchestration() -> None:
    """Verifies 12-step end-to-end Agency execution across Phases 1-6."""
    orch = SolopreneurAgencyOrchestrator()
    res = orch.execute_end_to_end_business_run(
        topic_keyword="AI Digital Automation",
        customer_email="buyer@solopreneur.ai",
        product_id="PROD-WORKFLOW-TEMPLATE",
        sale_amount_usd=299.0,
        ai_cost_usd=0.20,
    )
    assert res.order_amount_usd == 299.0
    assert res.net_profit_usd == 298.80
    assert res.roi_percentage > 100000.0
    assert res.architecture_drift == 0.0
    assert res.is_evidence_verified is True


def test_adaptive_environment_engine() -> None:
    """Verifies hardware and environment profiling."""
    engine = AdaptiveEnvironmentEngine()
    profile = engine.profile_and_adapt("SATELLITE_SPACECRAFT", True, 256)
    assert profile.execution_mode == ExecutionModeEnum.HARD_EMBEDDED_LOCAL


def test_ecosystem_integration_adapter() -> None:
    """Verifies Principle P12 ecosystem tool resolution."""
    engine = EcosystemIntegrationEngine()
    mapping = engine.resolve_tool_for_capability("governance")
    assert mapping.external_tool_name == "github_and_opa"


def test_legal_judicial_trial_execution() -> None:
    """Verifies legal governance trial execution."""
    uc = ConductArchitecturalTrialUseCase()
    verdict = uc.execute("packages/domain/models.py", True, "REMEDIATED")
    assert verdict.verdict == "ACQUITTED_COMPLIANT"


def test_zero_server_disaster_recovery() -> None:
    """Verifies cold re-hydration without server dependencies."""
    engine = ZeroServerDisasterRecoveryEngine()
    snap = engine.execute_cold_rehydration()
    assert snap.recovery_status == "100% RECOVERED_FROM_ZERO_SERVER"


def test_embedded_and_single_file_engines() -> None:
    """Verifies in-process embedded and single-file ACID engines."""
    emb = EAOSEmbeddedEngine()
    emb_res = emb.execute_in_process("marketing", "research")
    assert emb_res.in_process is True

    sf = EAOSSingleFileEngine("eaos_test_audit.db")
    sf_res = sf.execute_acid_transaction("TEST_ACTION", "hash123")
    assert sf_res.acid_compliant is True


def test_zero_cost_router_and_monetization() -> None:
    """Verifies zero-cost AI router and usage billing."""
    router = ZeroCostModelRouter()
    res = router.route_zero_cost_task("Generate Python Code")
    assert res.estimated_cost_usd == 0.0

    bill_uc = BillTenantUsageUseCase()
    entry = bill_uc.execute("TENANT_01", "marketing", 1000, 1000)
    assert entry.charge_usd > 0.0


def test_swarm_intelligence_orchestration() -> None:
    """Verifies biomimetic swarm agent spawning and pheromone emission."""
    uc = OrchestrateSwarmTaskUseCase()
    profile, signal = uc.execute(InsectRoleEnum.SPIDER_WEAVER, "knowledge_graph")
    assert profile.role == InsectRoleEnum.SPIDER_WEAVER
    assert signal.topic_target == "knowledge_graph"


def test_airgapped_deployment_compliance() -> None:
    """Verifies air-gapped zero-internet deployment profile."""
    engine = AirGappedDeploymentEngine()
    prof = AirGappedDeploymentProfileDTO(
        deployment_tier=DeploymentTierEnum.AIR_GAPPED,
        local_llm_endpoint="http://10.0.0.50:11434/v1",
        local_db_url="postgresql://eaos:sec@10.0.0.100:5432/eaos",
    )
    assert engine.evaluate_isolation_compliance(prof) is True


def test_enterprise_artifact_files_exist() -> None:
    """Verifies physical presence of declarative EA artifacts."""
    root = Path(".")
    assert (root / "infra" / "postgres" / "migrations" / "V001__init_eaos_schema.sql").exists()
    assert (root / "policies" / "security" / "rbac.rego").exists()
    assert (root / "contracts" / "proto" / "governance_v1.proto").exists()
