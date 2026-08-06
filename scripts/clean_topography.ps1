# Kịch bản PowerShell dọn dẹp các thư mục rác/cache trùng lặp
$ErrorActionPreference = "SilentlyContinue"
$RootDir = "D:\EAOS"

Write-Host ">>> Đang dọn dẹp các thư mục tạm và cache trên Monorepo..." -ForegroundColor Cyan

# 1. Xóa thư mục venvss trùng lặp (Giữ lại .venv chuẩn)
if (Test-Path "$RootDir\venvss") {
    Remove-Item -Path "$RootDir\venvss" -Recurse -Force
    Write-Host "✔ Đã xóa thư mục thừa: venvss" -ForegroundColor Green
}

# 2. Xóa các thư mục cache tạm thời
$CacheFolders = @(".pytest_tmp", ".coverage")
foreach ($folder in $CacheFolders) {
    if (Test-Path "$RootDir\$folder") {
        Remove-Item -Path "$RootDir\$folder" -Recurse -Force
        Write-Host "✔ Đã xóa cache: $folder" -ForegroundColor Green
    }
}

Write-Host ">>> Dọn dẹp Topography hoàn tất!" -ForegroundColor Cyan