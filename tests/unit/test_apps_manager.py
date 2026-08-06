"""Unit tests verifying production-ready AppsManager lifecycle orchestrator."""

from apps.apps_manager import AppsManager
from apps.models import AppLifecycleStatus, AppRegistrationDTO


def test_apps_manager_discovery() -> None:
    """Verify default 7 delivery channels are registered on initialization."""
    manager = AppsManager()
    matrix = manager.get_system_health_matrix()
    assert matrix.total_apps >= 7
    assert matrix.overall_system_status in ("HEALTHY", "DEGRADED")


def test_app_lifecycle_transitions() -> None:
    """Verify application start, stop, and health status transitions."""
    manager = AppsManager()
    app_id = "apps.api"

    # Start app
    started = manager.start_app(app_id)
    assert started is True

    health = manager.get_app_health(app_id)
    assert health is not None
    assert health.status == AppLifecycleStatus.HEALTHY
    assert health.health_score == 100

    # Stop app
    stopped = manager.stop_app(app_id)
    assert stopped is True

    health_stopped = manager.get_app_health(app_id)
    assert health_stopped is not None
    assert health_stopped.status == AppLifecycleStatus.STOPPED


def test_custom_app_registration() -> None:
    """Verify custom app registration DTO."""
    manager = AppsManager()
    custom_app = AppRegistrationDTO(
        app_id="apps.custom_channel",
        name="Custom Channel App",
        port=9000,
    )
    manager.register_app(custom_app)

    health = manager.get_app_health("apps.custom_channel")
    assert health is not None
    assert health.status == AppLifecycleStatus.REGISTERED