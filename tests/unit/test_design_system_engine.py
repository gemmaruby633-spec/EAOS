"""Unit tests verifying EAOS Design System Engine components."""

from pathlib import Path

import pytest
from designs.locales.i18n_engine import I18nCatalogEngine
from designs.tokens.engine import DesignTokenCompiler
from designs.ux.wcag_validator import WCAGAuditor


@pytest.fixture
def design_dir() -> Path:
    """Fixture trả về đường dẫn tới D:\\EAOS\\design."""
    return Path("D:/EAOS/design")


def test_token_compiler_loads_and_compiles(design_dir: Path) -> None:
    """Kiểm tra biên dịch Token sang CSS Variables."""
    compiler = DesignTokenCompiler(design_dir / "tokens")
    palette = compiler.load_palette()

    assert palette.primary.hex_value == "#06b6d4"
    assert palette.background.hex_value == "#0f172a"

    css = compiler.compile_to_css_variables(palette)
    assert "--color-primary: #06b6d4;" in css
    assert ":root {" in css


def test_wcag_auditor_contrast_ratio() -> None:
    """Kiểm tra động cơ tính toán độ tương phản WCAG 2.1."""
    auditor = WCAGAuditor()
    # Trắng (#ffffff) trên Đen (#000000) tỷ lệ phải xấp xỉ 21:1
    report = auditor.audit_contrast("#ffffff", "#000000")

    assert report.contrast_ratio == 21.0
    assert report.passes_aa_normal is True
    assert report.passes_aaa_normal is True

    # Chữ xám mờ trên nền đen kém tương phản
    low_contrast = auditor.audit_contrast("#333333", "#000000")
    assert low_contrast.passes_aaa_normal is False


def test_i18n_catalog_engine(design_dir: Path) -> None:
    """Kiểm tra động cơ dịch đa ngôn ngữ và nội suy tham số."""
    engine = I18nCatalogEngine(design_dir / "locales")
    engine.load_language("vi")

    title = engine.translate("vi", "title")
    assert title == "Hệ điều hành EAOS"