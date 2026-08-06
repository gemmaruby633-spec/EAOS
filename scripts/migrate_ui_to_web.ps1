$ErrorActionPreference = "SilentlyContinue"
$RootDir = "D:\EAOS"

Write-Host ">>> Đang di chuyển toàn bộ UI & Templates từ apps/api sang apps/web..." -ForegroundColor Cyan

# 1. Tạo cấu trúc thư mục chuẩn trong apps/web/web_app
New-Item -ItemType Directory -Force -Path "$RootDir\apps\web\web_app\templates" | Out-Null
New-Item -ItemType Directory -Force -Path "$RootDir\apps\web\web_app\routers" | Out-Null
New-Item -ItemType Directory -Force -Path "$RootDir\apps\web\web_app\presenters" | Out-Null

# 2. Chuyển Templates HTML sang apps/web
if (Test-Path "$RootDir\apps\api\app\templates") {
    Copy-Item -Path "$RootDir\apps\api\app\templates\*" -Destination "$RootDir\apps\web\web_app\templates" -Recurse -Force
    Remove-Item -Path "$RootDir\apps\api\app\templates" -Recurse -Force
    Write-Host "✔ Đã chuyên templates/ -> apps/web/web_app/templates" -ForegroundColor Green
}

# 3. Chuyển control_room_presenter.py sang apps/web
if (Test-Path "$RootDir\apps\api\app\presenters\control_room_presenter.py") {
    Move-Item -Path "$RootDir\apps\api\app\presenters\control_room_presenter.py" -Destination "$RootDir\apps\web\web_app\presenters\control_room_presenter.py" -Force
    Write-Host "✔ Đã chuyển control_room_presenter.py -> apps/web" -ForegroundColor Green
}

# 4. Chuyển control_room_router.py sang apps/web
if (Test-Path "$RootDir\apps\api\app\routers\control_room_router.py") {
    Move-Item -Path "$RootDir\apps\api\app\routers\control_room_router.py" -Destination "$RootDir\apps\web\web_app\routers\control_room_router.py" -Force
    Write-Host "✔ Đã chuyển control_room_router.py -> apps/web" -ForegroundColor Green
}

# 5. Dọn dẹp tệp router cũ trong apps/api
Remove-Item -Path "$RootDir\apps\api\app\routers\control_room.py" -ErrorAction SilentlyContinue
Remove-Item -Path "$RootDir\apps\api\app\routers\control_room_router.py" -ErrorAction SilentlyContinue

Write-Host "✔ [HOÀN TẤT] Đã tách biệt 100% UI sang apps/web!" -ForegroundColor Green