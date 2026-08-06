"""Unit tests verifying production-ready Locales i18n Manager."""

from locales.manager import LocalesManager


def test_locales_manager_supported_languages() -> None:
    """Verify all 3 language catalogs (vi, en, ja) are correctly loaded."""
    manager = LocalesManager()
    locales = manager.get_supported_locales()
    assert "vi" in locales
    assert "en" in locales
    assert "ja" in locales


def test_translation_key_lookup_and_interpolation() -> None:
    """Verify dot-separated key lookup, parameter interpolation and fallback."""
    manager = LocalesManager()

    # Vietnamese Title
    title_vi = manager.translate("system.title", locale="vi")
    assert title_vi == "Hệ điều hành Kiến trúc Doanh nghiệp EAOS"

    # English Title
    title_en = manager.translate("system.title", locale="en")
    assert title_en == "EAOS Enterprise Architecture Operating System"

    # Japanese Title
    title_ja = manager.translate("system.title", locale="ja")
    assert "オペレーティングシステム" in title_ja

    # Interpolation
    welcome_vi = manager.translate(
        "system.welcome", locale="vi", name="Solopreneur"
    )
    assert welcome_vi == "Xin chào Solopreneur"

    welcome_en = manager.translate(
        "system.welcome", locale="en", name="Solopreneur"
    )
    assert welcome_en == "Welcome Solopreneur"


def test_translation_missing_key_fallback() -> None:
    """Verify missing keys return the raw key path without failing."""
    manager = LocalesManager()
    missing = manager.translate("non.existent.key.path", locale="vi")
    assert missing == "non.existent.key.path"


def test_catalog_schema_validation() -> None:
    """Verify Pydantic schema validation returns structured model."""
    manager = LocalesManager()
    schema_vi = manager.get_catalog_schema("vi")
    assert schema_vi is not None
    assert schema_vi.language_code == "vi"
    assert schema_vi.auth.login == "Đăng nhập"