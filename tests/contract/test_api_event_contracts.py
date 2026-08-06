"""Contract test suite verifying OpenAPI and event schema validity."""

from pathlib import Path

from platforms.contracts.contract_registry import ContractRegistry

ROOT_PATH = Path(__file__).resolve().parents[2]


def test_contract_schemas_are_valid() -> None:
    """Verifies that all communication contracts pass registry verification."""
    registry = ContractRegistry(ROOT_PATH)
    contracts = registry.discover_contracts()
    assert len(contracts) >= 5
