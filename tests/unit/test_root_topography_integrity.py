"""Unit tests auditing root topography integrity of EAOS Monorepo."""

from pathlib import Path

from tools.doctor.topography_mapper import (
    ArchitectureRing,
    EAOSTopographyAuditor,
)


def test_audit_root_topography_rings() -> None:
    """Kiểm tra công cụ phân loại địa hình hoạt động chính xác."""
    auditor = EAOSTopographyAuditor()
    root_path = Path("D:/EAOS")

    if root_path.exists():
        infos = auditor.audit_workspace_root(root_path)
        folder_names = {info.name for info in infos}

        # Đảm bảo các thư mục lõi quan trọng có mặt tại Root
        assert "apps" in folder_names
        assert "kernel" in folder_names
        assert "packages" in folder_names
        assert "docs" in folder_names


def test_cache_folders_classification() -> None:
    """Đảm bảo venvss và .pytest_tmp được phân loại đúng là TEMPORARY_CACHE."""
    auditor = EAOSTopographyAuditor()
    assert auditor.RING_MAPPING["venvss"] == ArchitectureRing.TEMPORARY_CACHE
    assert (
        auditor.RING_MAPPING[".pytest_tmp"]
        == ArchitectureRing.TEMPORARY_CACHE
    )