$ErrorActionPreference = "Stop"
$RootDir = "D:\EAOS"

Write-Host ">>> Đang tạo pyproject.toml cho kernel, engine, tools..." -ForegroundColor Cyan

# 1. Tạo pyproject.toml cho kernel (eaos-kernel)
$KernelToml = "$RootDir\kernel\pyproject.toml"
if (-not (Test-Path $KernelToml)) {
    $KernelContent = @"
[project]
name = "eaos-kernel"
version = "0.1.0"
description = "EAOS Immutable Kernel Package"
readme = "README.md"
requires-python = ">=3.14"

dependencies = []

[build-system]
requires = ["hatchling>=1.28"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["."]
"@
    Set-Content -Path $KernelToml -Value $KernelContent -Encoding UTF8
    Write-Host "✔ Đã tạo kernel/pyproject.toml (name = 'eaos-kernel')" -ForegroundColor Green
}

# 2. Tạo pyproject.toml cho engine (eaos-engine)
$EngineToml = "$RootDir\engine\pyproject.toml"
if (-not (Test-Path $EngineToml)) {
    $EngineContent = @"
[project]
name = "eaos-engine"
version = "0.1.0"
description = "EAOS Execution Engine Package"
readme = "README.md"
requires-python = ">=3.14"

dependencies = []

[build-system]
requires = ["hatchling>=1.28"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["."]
"@
    Set-Content -Path $EngineToml -Value $EngineContent -Encoding UTF8
    Write-Host "✔ Đã tạo engine/pyproject.toml (name = 'eaos-engine')" -ForegroundColor Green
}

# 3. Tạo pyproject.toml cho tools (eaos-tools)
$ToolsToml = "$RootDir\tools\pyproject.toml"
if (-not (Test-Path $ToolsToml)) {
    $ToolsContent = @"
[project]
name = "eaos-tools"
version = "0.1.0"
description = "EAOS Engineering Tools Package"
readme = "README.md"
requires-python = ">=3.14"

dependencies = []

[build-system]
requires = ["hatchling>=1.28"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["."]
"@
    Set-Content -Path $ToolsToml -Value $ToolsContent -Encoding UTF8
    Write-Host "✔ Đã tạo tools/pyproject.toml (name = 'eaos-tools')" -ForegroundColor Green
}

# 4. Cập nhật root pyproject.toml bổ sung dependencies & sources
$RootToml = "$RootDir\pyproject.toml"
if (Test-Path $RootToml) {
    $RootContent = Get-Content -Path $RootToml -Raw
    
    # Bổ sung eaos-kernel, eaos-engine, eaos-tools nếu chưa có
    if ($RootContent -notmatch '"eaos-kernel"') {
        $RootContent = $RootContent -replace '"eaos-platforms",', '"eaos-platforms",`n    "eaos-kernel",`n    "eaos-engine",`n    "eaos-tools",'
        $RootContent = $RootContent -replace 'eaos-platforms = \{ workspace = true \}', "eaos-platforms = { workspace = true }`neaos-kernel = { workspace = true }`neaos-engine = { workspace = true }`neaos-tools = { workspace = true }"
        Set-Content -Path $RootToml -Value $RootContent -Encoding UTF8
        Write-Host "✔ Đã cập nhật root pyproject.toml bổ sung eaos-kernel, eaos-engine, eaos-tools" -ForegroundColor Green
    }
}

Write-Host ">>> Khởi tạo pyproject.toml cho các thư mục lớn hoàn tất!" -ForegroundColor Cyan