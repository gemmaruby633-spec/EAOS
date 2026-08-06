"""Unit tests verifying production-ready Design System engines."""

from designs.components.component_engine import UIComponentEngine
from designs.fonts.font_engine import FontEngine, FontSpec
from designs.locales.i18n_engine import I18nEngine
from designs.public.manifest_engine import ManifestEngine
from designs.styles.token_engine import TokenEngine
from designs.ux.wcag_auditor import WCAGAuditor


def test_i18n_engine_translation_and_fallback() -> None:
    """Verify translation, string interpolation and fallback mechanisms."""
    engine = I18nEngine()
    
    # Vietnamese
    vi_title = engine.translate("system.title", locale="vi")
    assert vi_title == "Hệ điều hành EAOS"
    
    # Interpolation
    welcome_vi = engine.translate("system.welcome", locale="vi", name="Solopreneur")
    assert welcome_vi == "Xin chào Solopreneur"
    
    # Fallback to key
    missing = engine.translate("unknown.key.string", locale="vi")
    assert missing == "unknown.key.string"


def test_token_engine_css_variable_generation() -> None:
    """Verify token engine produces valid CSS variables."""
    engine = TokenEngine()
    css = engine.generate_css_variables()
    assert "--color-primary: #06b6d4;" in css
    assert "--color-background: #0f172a;" in css


def test_component_engine_rendering() -> None:
    """Verify Jinja2 component rendering for buttons, cards, and badges."""
    engine = UIComponentEngine()
    btn_html = engine.render_button(label="Thực thi", variant="primary")
    assert "bg-cyan-600" in btn_html
    assert "Thực thi" in btn_html

    card_html = engine.render_card(title="Tiêu đề", content="Nội dung")
    assert "Tiêu đề" in card_html
    assert "Nội dung" in card_html


def test_wcag_auditor_contrast_ratio() -> None:
    """Verify WCAG 2.1 color contrast calculation for high vs low contrast."""
    # High contrast: White text on Dark background
    result_high = WCAGAuditor.audit_contrast(fg_hex="#ffffff", bg_hex="#0f172a")
    assert result_high.contrast_ratio >= 10.0
    assert result_high.passes_aa_normal is True
    assert result_high.passes_aaa_normal is True

    # Low contrast: Dark gray on Black background
    result_low = WCAGAuditor.audit_contrast(fg_hex="#1e293b", bg_hex="#0f172a")
    assert result_low.passes_aa_normal is False


def test_manifest_and_font_engine() -> None:
    """Verify PWA manifest serialization and font-face CSS generation."""
    manifest_engine = ManifestEngine()
    json_manifest = manifest_engine.to_json()
    assert "EAOS Enterprise Operating System" in json_manifest

    font_engine = FontEngine()
    font_engine.register_font(FontSpec(family="Inter", file_name="inter.woff2"))
    font_css = font_engine.generate_font_face_css()
    assert "font-family: 'Inter';" in font_css