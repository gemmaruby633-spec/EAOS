# Đường dẫn file compose và prometheus
$composeFile = "D:\EAOS\infra\compose\docker-compose.prod.yml"
$prometheusFile = "D:\EAOS\infra\compose\observability\prometheus\prometheus.yaml"

# 1. Thêm service Node Exporter vào docker-compose.prod.yml nếu chưa có
$composeContent = Get-Content $composeFile -Raw
if ($composeContent -notmatch "node-exporter") {
    Add-Content $composeFile @"
  node-exporter:
    image: prom/node-exporter:latest
    container_name: eaos-node-exporter
    restart: always
    ports:
      - "9100:9100"
"@
    Write-Host "✅ Đã thêm service Node Exporter vào docker-compose.prod.yml" -ForegroundColor Green
}

# 2. Thêm scrape job cho Node Exporter vào prometheus.yaml nếu chưa có
$promContent = Get-Content $prometheusFile -Raw
if ($promContent -notmatch "job_name: 'node'") {
    Add-Content $prometheusFile @"
- job_name: 'node'
  static_configs:
    - targets: ['eaos-node-exporter:9100']
"@
    Write-Host "✅ Đã thêm scrape job Node Exporter vào prometheus.yaml" -ForegroundColor Green
}

# 3. Khởi động lại stack để áp dụng
docker-compose -f $composeFile up -d --remove-orphans

# 4. Restart Prometheus để đọc lại config
docker-compose -f $composeFile restart prometheus

Write-Host "🎯 Node Exporter đã sẵn sàng. Mở http://localhost:9100/metrics để kiểm tra, và Grafana sẽ hiển thị dữ liệu hệ thống." -ForegroundColor Cyan
