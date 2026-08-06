# EAOS 1-Click Production Daemon Launcher
$ErrorActionPreference = "Stop"
Set-Location -Path "D:\EAOS"

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host " EAOS 24/7 Production Daemon Control Launcher       " -ForegroundColor Cyan
Write-Host " Workspace: D:\EAOS                                " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

# Check Docker Engine
try {
    docker ps | Out-Null
    Write-Host "✔ Docker Engine is active and running." -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Engine is not running! Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Start Production Stack
Write-Host "`n---> Launching Production Stack Containers in Background (24/7)..." -ForegroundColor Yellow
docker compose -f infra/compose/docker-compose.prod.yml up -d

Write-Host "`n====================================================" -ForegroundColor Cyan
Write-Host " EAOS PRODUCTION DAEMON STACK ACTIVE 24/7!          " -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Cyan
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"