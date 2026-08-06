"""Security identity package."""

from __future__ import annotations

from .iam_policy import IAMPolicy, IAMPolicyEngine

IamEngine = IAMPolicyEngine

__all__ = ["IAMPolicy", "IAMPolicyEngine", "IamEngine"]
