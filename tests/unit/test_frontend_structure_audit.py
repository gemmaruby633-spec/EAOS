"""Unit tests auditing complete file existence of EAOS Frontend."""

from pathlib import Path


def test_frontend_directory_and_files_exist() -> None:
    """Kiểm tra toàn bộ thư mục và tệp tin mã nguồn của Frontend."""
    frontend_dir = Path("D:/EAOS/frontend")

    required_files = [
        frontend_dir / "package.json",
        frontend_dir / "tsconfig.json",
        frontend_dir / "README.md",
        frontend_dir / "src" / "App.tsx",
        frontend_dir / "src" / "index.tsx",
        frontend_dir / "src" / "types" / "index.ts",
        frontend_dir / "src" / "utils" / "cn.ts",
        frontend_dir / "src" / "services" / "apiClient.ts",
        frontend_dir / "src" / "hooks" / "useSSE.ts",
        frontend_dir / "src" / "store" / "useAppStore.ts",
        frontend_dir / "src" / "layouts" / "MainLayout.tsx",
        frontend_dir / "src" / "routes" / "AppRoutes.tsx",
        frontend_dir / "src" / "components" / "ui" / "Button.tsx",
        frontend_dir / "src" / "features" / "control-room" / "ControlRoomFeature.tsx",
        frontend_dir / "src" / "features" / "knowledge" / "KnowledgeFeature.tsx",
    ]

    for file_path in required_files:
        assert file_path.exists(), f"Thiếu tệp tin bắt buộc: {file_path}"