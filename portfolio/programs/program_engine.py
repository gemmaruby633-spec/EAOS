"""Động cơ quản lý Chương trình và Đồ thị Phụ thuộc."""

from __future__ import annotations

from programs.models import PortfolioProgram


class ProgramEngine:
    """Quản lý phụ thuộc giữa các Chương trình."""

    def __init__(self) -> None:
        self._programs: dict[str, PortfolioProgram] = {}

    def register_program(
        self,
        program_id: str,
        name: str,
        lead_architect: str,
    ) -> PortfolioProgram:
        """Đăng ký Chương trình mới."""
        prog = PortfolioProgram(
            program_id=program_id,
            name=name,
            lead_architect=lead_architect,
        )
        self._programs[program_id] = prog
        return prog

    def add_dependency(
        self,
        program_id: str,
        depends_on_id: str,
    ) -> None:
        """Thêm phụ thuộc vào đồ thị chương trình."""
        if program_id not in self._programs:
            raise KeyError(f"Program {program_id} không tồn tại.")
        self._programs[program_id].dependencies.append(depends_on_id)
