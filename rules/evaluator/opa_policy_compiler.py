"""Trình biên dịch quy tắc YAML sang mã OPA Rego Policy."""

from __future__ import annotations


class OpaPolicyCompiler:
    """Biên dịch định nghĩa quy tắc sang chuẩn Open Policy Agent."""

    @staticmethod
    def compile_to_rego(package_name: str, rule_id: str) -> str:
        """Sinh mã Rego Policy mẫu."""
        return (
            f"package eaos.rules.{package_name}\n\n"
            f"default allow = false\n\n"
            f"allow {{\n"
            f'    input.rule_id == "{rule_id}"\n'
            f"    input.violation_count == 0\n"
            f"}}\n"
        )
