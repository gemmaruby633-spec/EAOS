"""Động cơ máy trạng thái hữu hạn (FSM Machine)."""

from __future__ import annotations


class FsmStateEngine:
    """Quản lý chuyển đổi trạng thái FSM."""

    def __init__(self, initial_state: str = "READY") -> None:
        self.current_state = initial_state

    def transition_to(self, new_state: str) -> str:
        """Chuyển sang trạng thái mới."""
        self.current_state = new_state
        return self.current_state
