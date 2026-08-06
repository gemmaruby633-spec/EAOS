"""Mô hình DTO Customer Relationship Management (CRM)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class LeadStage(StrEnum):
    """Các giai đoạn của Lead CRM."""

    NEW = "NEW"
    QUALIFIED = "QUALIFIED"
    PROPOSAL = "PROPOSAL"
    WON = "WON"
    LOST = "LOST"


@dataclass
class CustomerLead:
    """Mô hình Lead/Khách hàng tiềm năng."""

    lead_id: str
    company_name: str
    contact_email: str
    estimated_value: float
    stage: LeadStage = LeadStage.NEW
