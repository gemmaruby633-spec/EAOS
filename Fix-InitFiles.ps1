# ==========================================
# EAOS Automatic __init__.py Generator Script
# ==========================================

Write-Host "1. Scanning EAOS Monorepo to ensure all Python package directories have __init__.py..." -ForegroundColor Cyan

$rootPath = Get-Location
$excludedDirs = @('.venv', '.git', '.mypy_cache', '.pytest_cache', '.ruff_cache', 'build', 'dist', 'generated', 'runtime', '.vscode', '.github', '.agents', 'frontend')

# Lấy tất cả các thư mục con trong workspace
$directories = Get-ChildItem -Path $rootPath -Recurse -Directory | Where-Object {
    $dirName = $_.Name
    $fullName = $_.FullName
    
    # Kiểm tra xem đường dẫn có nằm trong danh sách loại trừ không
    $isExcluded = $false
    foreach ($ex in $excludedDirs) {
        if ($fullName -like "*\$ex*" -or $fullName -eq "$rootPath\$ex") {
            $isExcluded = $true
            break
        }
    }
    return -not $isExcluded
}

$count = 0
foreach ($dir in $directories) {
    # Kiểm tra xem thư mục có chứa ít nhất một file .py nào không
    $pyFiles = Get-ChildItem -Path $dir.FullName -Filter "*.py" -File
    if ($pyFiles.Count -gt 0) {
        $initPath = Join-Path $dir.FullName "__init__.py"
        if (-not (Test-Path $initPath)) {
            # Tạo file __init__.py chuẩn kèm docstring an toàn cho MyPy
            $content = '"""Package initialization module."""'
            Set-Content -Path $initPath -Value $content -Encoding UTF8
            Write-Host "Created missing __init__.py in: $($dir.FullName)" -ForegroundColor Green
            $count++
        }
    }
}

Write-Host "`n[SUCCESS] Successfully scanned monorepo and created $count missing __init__.py files!" -ForegroundColor Yellow
Write-Host "You can now run: uv run task lint" -ForegroundColor Cyan