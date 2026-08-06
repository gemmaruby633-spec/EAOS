Write-Host "🏛️ Đang kiểm toán Ranh giới Kiến trúc Hexagonal (AST Validation)..." -ForegroundColor Yellow
uv run python -m TOOLS.cli.main validate

Write-Host "`n🩺 Đang kiểm tra Sức khỏe Hạ tầng Doctor v2 Diagnostic..." -ForegroundColor Yellow
uv run python -m TOOLS.cli.main doctor