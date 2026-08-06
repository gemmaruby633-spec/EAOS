<#
.SYNOPSIS
    Fix-EAOS-Structure.ps1
    Kịch bản tự động sửa lỗi Mypy Namespace và tự động dò tìm (Auto-discover) tệp chứa Class để Re-export chuẩn xác.
#>

$ErrorActionPreference = "Stop"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

Write-Host "=== 1. ĐỒNG BỘ CẤU HÌNH MYPY TRONG PYPROJECT.TOML ===" -ForegroundColor Cyan
$pyprojectPath = "pyproject.toml"
if (Test-Path $pyprojectPath) {
    $content = [System.IO.File]::ReadAllText($pyprojectPath)
    
    # Sửa hoặc thêm mypy_path chỉ chứa root ["."]
    if ($content -match 'mypy_path\s*=\s*\[[^\]]*\]') {
        $content = $content -replace 'mypy_path\s*=\s*\[[^\]]*\]', 'mypy_path = ["."]'
    } else {
        $content = $content -replace '\[tool\.mypy\]', "[tool.mypy]`nmypy_path = [`".`"]"
    }

    # Bắt buộc bật explicit_package_bases
    if ($content -notmatch 'explicit_package_bases\s*=\s*true') {
        $content = $content -replace '\[tool\.mypy\]', "[tool.mypy]`nexplicit_package_bases = true"
    }

    [System.IO.File]::WriteAllText($pyprojectPath, $content, $Utf8NoBom)
    Write-Host "[FIXED] Đã ép buộc mypy_path = [`".`"] trong pyproject.toml" -ForegroundColor Green
}

Write-Host "`n=== 2. AUTO-DISCOVER & RE-EXPORT CHO GOVERNANCE PORTS ===" -ForegroundColor Cyan
$portsDir = "packages\governance\domain\ports"
$portFile = Get-ChildItem -Path $portsDir -Filter "*.py" -Recurse | 
    Where-Object { $_.Name -ne "__init__.py" -and (Get-Content $_.FullName -Raw) -match "KnowledgeGraphPort" } | 
    Select-Object -First 1

if ($portFile) {
    $baseDir = (Get-Location).Path + "\"
    $relativePath = $portFile.FullName.Replace($baseDir, "").Replace("\", ".").Replace(".py", "")
    $portsInitContent = @"
"""Governance Domain Ports Package."""

from $relativePath import KnowledgeGraphPort

__all__ = ["KnowledgeGraphPort"]
"@
    [System.IO.File]::WriteAllText("$portsDir\__init__.py", $portsInitContent, $Utf8NoBom)
    Write-Host "[FIXED] Re-export KnowledgeGraphPort từ module: $relativePath" -ForegroundColor Green
} else {
    Write-Warning "[WARN] Không tìm thấy tệp chứa KnowledgeGraphPort trong $portsDir"
}

Write-Host "`n=== 3. AUTO-DISCOVER & RE-EXPORT CHO GOVERNANCE USE CASES ===" -ForegroundColor Cyan
$useCasesDir = "packages\governance\application\use_cases"
$useCaseFile = Get-ChildItem -Path $useCasesDir -Filter "*.py" -Recurse | 
    Where-Object { $_.Name -ne "__init__.py" -and (Get-Content $_.FullName -Raw) -match "EvaluateGovernanceUseCase" } | 
    Select-Object -First 1

if ($useCaseFile) {
    $baseDir = (Get-Location).Path + "\"
    $relativePath = $useCaseFile.FullName.Replace($baseDir, "").Replace("\", ".").Replace(".py", "")
    $useCasesInitContent = @"
"""Governance Application Use Cases Package."""

from $relativePath import EvaluateGovernanceUseCase

__all__ = ["EvaluateGovernanceUseCase"]
"@
    [System.IO.File]::WriteAllText("$useCasesDir\__init__.py", $useCasesInitContent, $Utf8NoBom)
    Write-Host "[FIXED] Re-export EvaluateGovernanceUseCase từ module: $relativePath" -ForegroundColor Green
} else {
    Write-Warning "[WARN] Không tìm thấy tệp chứa EvaluateGovernanceUseCase trong $useCasesDir"
}

Write-Host "`n=== 4. THỰC THI KIỂM THỬ LINTING VÀ TEST SUITE ===" -ForegroundColor Cyan
uv run task lint
uv run task test