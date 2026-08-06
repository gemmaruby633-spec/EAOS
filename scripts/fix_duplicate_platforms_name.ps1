$ErrorActionPreference = "Stop"
$RootDir = "D:\EAOS"

Write-Host ">>> Đang sửa lỗi trùng tên workspace member eaos-platforms..." -ForegroundColor Cyan

# 1. Đổi tên package trong packages/platforms/pyproject.toml
$PkgPlatformsToml = "$RootDir\packages\platforms\pyproject.toml"

if (Test-Path $PkgPlatformsToml) {
    $Content = Get-Content -Path $PkgPlatformsToml -Raw
    # Thay thế name = "eaos-platforms" thành name = "eaos-packages-platforms"
    $UpdatedContent = $Content -replace 'name\s*=\s*"eaos-platforms"', 'name = "eaos-packages-platforms"'
    Set-Content -Path $PkgPlatformsToml -Value $UpdatedContent -Encoding UTF8
    Write-Host "✔ Đã cập nhật packages/platforms/pyproject.toml -> name = 'eaos-packages-platforms'" -ForegroundColor Green
}

# 2. Cập nhật pyproject.toml gốc ở D:\EAOS
$RootToml = "$RootDir\pyproject.toml"
if (Test-Path $RootToml) {
    $RootContent = Get-Content -Path $RootToml -Raw
    
    # Bổ sung eaos-packages-platforms vào dependencies nếu chưa có
    if ($RootContent -notmatch '"eaos-packages-platforms"') {
        $RootContent = $RootContent -replace '"eaos-platforms",', '"eaos-platforms",`n    "eaos-packages-platforms",'
        $RootContent = $RootContent -replace 'eaos-platforms = \{ workspace = true \}', "eaos-platforms = { workspace = true }`neaos-packages-platforms = { workspace = true }"
        Set-Content -Path $RootToml -Value $RootContent -Encoding UTF8
        Write-Host "✔ Đã cập nhật root pyproject.toml bổ sung eaos-packages-platforms" -ForegroundColor Green
    }
}

Write-Host ">>> Sửa lỗi trùng tên hoàn tất!" -ForegroundColor Cyan