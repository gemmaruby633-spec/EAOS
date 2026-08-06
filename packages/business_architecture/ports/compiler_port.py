"""Enterprise Model Compiler Parser Port Protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from packages.business_architecture.domain.compiler_models import (
    BusinessSpecificationIR,
)


@runtime_checkable
class BusinessSpecParserPort(Protocol):
    """Port protocol for parsing YAML/DSL business specifications."""

    async def parse_yaml_spec(self, yaml_content: str) -> BusinessSpecificationIR: ...

    async def parse_spec_file(self, file_path: str) -> BusinessSpecificationIR: ...
