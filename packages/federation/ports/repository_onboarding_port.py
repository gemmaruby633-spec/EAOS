"""External Repository Onboarding Port Protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from packages.federation.domain.repository_onboarding_models import (
    ExternalRepositoryDTO,
    OnboardingReportDTO,
)


@runtime_checkable
class RepositoryOnboardingPort(Protocol):
    """Port protocol for dynamic multi-repository installation."""

    async def install_repository(self, repo_slug_or_url: str) -> OnboardingReportDTO: ...

    def list_installed_repositories(self) -> list[ExternalRepositoryDTO]: ...
