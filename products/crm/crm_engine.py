"""Động cơ CRM quản lý phễu khách hàng."""

from __future__ import annotations

from crm.models import CustomerLead, LeadStage


class CrmEngine:
    """Động cơ quản lý quan hệ khách hàng và leads."""

    def __init__(self) -> None:
        self._leads: dict[str, CustomerLead] = {}

    def register_lead(
        self,
        lead_id: str,
        company_name: str,
        contact_email: str,
        value: float,
    ) -> CustomerLead:
        """Đăng ký lead mới."""
        lead = CustomerLead(
            lead_id=lead_id,
            company_name=company_name,
            contact_email=contact_email,
            estimated_value=value,
        )
        self._leads[lead_id] = lead
        return lead

    def advance_stage(self, lead_id: str, new_stage: LeadStage) -> CustomerLead:
        """Chuyển giai đoạn xử lý lead."""
        if lead_id not in self._leads:
            raise KeyError(f"Lead {lead_id} không tồn tại.")
        lead = self._leads[lead_id]
        lead.stage = new_stage
        return lead
