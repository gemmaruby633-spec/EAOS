Write-Host "🔍 [1/2] Đang chạy Ruff Linter..." -ForegroundColor Yellow
uv run python -m ruff check --fix --unsafe-fixes .

Write-Host "`n🔍 [2/2] Đang chạy Mypy Strict Typechecker..." -ForegroundColor Yellow
uv run python -m mypy apps kernel engine packages tools tests platforms PORTFOLIO