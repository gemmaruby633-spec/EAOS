<#
.SYNOPSIS
    Patch-CodeInFile.ps1
    Kịch bản tự động khắc phục toàn bộ lỗi Namespace, Re-export, Cấu hình Mypy/Pytest và mã hóa UTF-8 No-BOM.
#>

$ErrorActionPreference = "Stop"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Write-Utf8File {
    param (
        [string]$Path,
        [string]$Content
    )
    $parent = Split-Path -Parent $Path
    if (-not (Test-Path $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    [System.IO.File]::WriteAllText($Path, $Content, $script:Utf8NoBom)
    Write-Host "[FIXED/CREATED] $Path" -ForegroundColor Green
}

Write-Host "=== 1. KHÔI PHỤC CẤU TRÚC PACKAGE NAMESPACE ===" -ForegroundColor Cyan

# Tạo tất cả các file __init__.py trung gian bắt buộc
$initFiles = @(
    "packages\governance\__init__.py",
    "packages\governance\domain\__init__.py",
    "packages\governance\application\__init__.py",
    "packages\reflection\__init__.py",
    "packages\reflection\application\__init__.py"
)

foreach ($file in $initFiles) {
    if (-not (Test-Path $file)) {
        Write-Utf8File -Path $file -Content '"""Namespace package initialization."""'
    }
}

Write-Host "=== 2. GHI NỘI DUNG RE-EXPORT CHUẨN (UTF-8 NO-BOM) ===" -ForegroundColor Cyan

# Ghi file Re-export Domain Ports
$portsContent = @"
"""Governance Domain Ports Package."""

from packages.governance.domain.ports.knowledge_graph import KnowledgeGraphPort

__all__ = ["KnowledgeGraphPort"]
"@
Write-Utf8File -Path "packages\governance\domain\ports\__init__.py" -Content $portsContent

# Ghi file Re-export Application Use Cases
$useCasesContent = @"
"""Governance Application Use Cases Package."""

from packages.governance.application.use_cases.evaluate_governance import (
    EvaluateGovernanceUseCase,
)

__all__ = ["EvaluateGovernanceUseCase"]
"@
Write-Utf8File -Path "packages\governance\application\use_cases\__init__.py" -Content $useCasesContent

Write-Host "=== 3. CẬP NHẬT CẤU HÌNH PYPROJECT.TOML ===" -ForegroundColor Cyan

$pyprojectPath = "pyproject.toml"
if (Test-Path $pyprojectPath) {
    $pyprojectText = [System.IO.File]::ReadAllText($pyprojectPath)
    $updated = $false

    # Cập nhật hoặc bổ sung cấu hình [tool.mypy]
    if ($pyprojectText -notmatch "explicit_package_bases\s*=\s*true") {
        if ($pyprojectText -match "\[tool\.mypy\]") {
            $pyprojectText = $pyprojectText -replace "\[tool\.mypy\]", "[tool.mypy]`nexplicit_package_bases = true`nmypy_path = `".`""
        } else {
            $pyprojectText += "`n`n[tool.mypy]`nexplicit_package_bases = true`nmypy_path = `".`"`n"
        }
        $updated = $true
    }

    # Cập nhật hoặc bổ sung cấu hình [tool.pytest.ini_options]
    if ($pyprojectText -notmatch "\[tool\.pytest\.ini_options\]") {
        $pyprojectText += "`n`n[tool.pytest.ini_options]`npythonpath = [`".`"]`ntestpaths = [`"tests`"]`n"
        $updated = $true
    } elseif ($pyprojectText -notmatch "pythonpath\s*=\s*\[") {
        $pyprojectText = $pyprojectText -replace "\[tool\.pytest\.ini_options\]", "[tool.pytest.ini_options]`npythonpath = [`".`"]"
        $updated = $true
    }

    if ($updated) {
        Write-Utf8File -Path $pyprojectPath -Content $pyprojectText
    } else {
        Write-Host "[SKIP] pyproject.toml đã có đủ cấu hình chuẩn." -ForegroundColor Yellow
    }
}

Write-Host "=== 4. CHẠY TEST SUITE VÀ LINTER ===" -ForegroundColor Cyan
uv run task lint
uv run task test