# EAOS Auto-Repair Script
Write-Host "=== EAOS Auto-Repair Script ===" -ForegroundColor Cyan

# 1. Đảm bảo thư mục tmpdir tồn tại
if (-not (Test-Path "D:\EAOS\tmp\pytest")) {
    Write-Host "Creating tmpdir for pytest..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path "D:\EAOS\tmp\pytest" | Out-Null
}

# 2. Đặt TMP/TEMP cho pytest
$env:TMP="D:\EAOS\tmp"
$env:TEMP="D:\EAOS\tmp"

# 3. Format codebase với Ruff
Write-Host "Running Ruff format..." -ForegroundColor Yellow
python -m ruff format .

# 4. Lint (Ruff + Mypy)
Write-Host "Running lint checks..." -ForegroundColor Yellow
python -m ruff check --fix --unsafe-fixes .
python -m mypy apps/ kernel/ engine/ packages/ tools/ tests/ platform_services/

# 5. Test với pytest (dùng basetemp riêng)
Write-Host "Running pytest suite..." -ForegroundColor Yellow
python -m pytest tests/

# 6. Validator EAOS
Write-Host "Running EAOS Architecture Validator..." -ForegroundColor Yellow
python -m apps.cli.main validate

Write-Host "=== Auto-Repair Completed ===" -ForegroundColor Green

