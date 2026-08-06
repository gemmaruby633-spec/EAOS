"""Package quản lý quan hệ khách hàng CRM."""

from crm.crm_engine import CrmEngine
from crm.models import CustomerLead, LeadStage

__all__ = ["CrmEngine", "CustomerLead", "LeadStage"]
