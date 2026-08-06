Write-Host "🧪 Đang chạy Pytest Unit Test Suite..." -ForegroundColor Yellow
uv run python -m pytest tests --basetemp=.pytest_tmp -v