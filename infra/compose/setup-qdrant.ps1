# Bước 1: Thêm service Qdrant vào docker-compose.prod.yml nếu chưa có
$composeFile = "D:\EAOS\infra\compose\docker-compose.prod.yml"
$composeContent = Get-Content $composeFile -Raw

if ($composeContent -notmatch "eaos-qdrant") {
    Add-Content $composeFile @"
  eaos-qdrant:
    image: qdrant/qdrant:latest
    container_name: eaos-qdrant
    restart: always
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
"@
    Write-Host "✅ Đã thêm service Qdrant vào docker-compose.prod.yml" -ForegroundColor Green
}

# Bước 2: Khởi động lại stack
docker-compose -f $composeFile up -d --remove-orphans

# Chờ container Qdrant khởi động
Start-Sleep -Seconds 10

# Bước 3: Tạo collection demo
Invoke-WebRequest -Uri "http://localhost:6333/collections/demo_collection" `
    -Method Put `
    -ContentType "application/json" `
    -Body '{"vectors": {"size": 4, "distance": "Cosine"}}'

# Bước 4: Insert vector mẫu
Invoke-WebRequest -Uri "http://localhost:6333/collections/demo_collection/points?wait=true" `
    -Method Put `
    -ContentType "application/json" `
    -Body '{"points":[{"id":1,"vector":[0.1,0.2,0.3,0.4],"payload":{"tag":"demo"}}]}'

Write-Host "🎯 Qdrant đã sẵn sàng với collection demo và dữ liệu mẫu. Mở http://localhost:6333/dashboard#/welcome để xem." -ForegroundColor Cyan
