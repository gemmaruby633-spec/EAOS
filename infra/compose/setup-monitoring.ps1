# Tạo thư mục provisioning cho Grafana
$grafanaProvisioning = "D:\EAOS\infra\compose\observability\grafana\provisioning"
New-Item -ItemType Directory -Force -Path "$grafanaProvisioning\datasources"
New-Item -ItemType Directory -Force -Path "$grafanaProvisioning\dashboards"
New-Item -ItemType Directory -Force -Path "$grafanaProvisioning\dashboards\files"

# Datasource.yaml
@"
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://eaos-prometheus:9090
    isDefault: true
"@ | Set-Content "$grafanaProvisioning\datasources\datasource.yaml"

# Dashboard.yaml
@"
apiVersion: 1
providers:
  - name: 'EAOS Dashboards'
    orgId: 1
    folder: 'EAOS Monitoring'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 30
    options:
      path: /etc/grafana/provisioning/dashboards/files
"@ | Set-Content "$grafanaProvisioning\dashboards\dashboard.yaml"

# Tải dashboard JSON từ Grafana.com
Invoke-WebRequest -Uri "https://grafana.com/api/dashboards/9628/revisions/1/download" -OutFile "$grafanaProvisioning\dashboards\files\postgres-dashboard.json"
Invoke-WebRequest -Uri "https://grafana.com/api/dashboards/763/revisions/1/download" -OutFile "$grafanaProvisioning\dashboards\files\redis-dashboard.json"

Write-Host "✅ Datasource và Dashboard đã được cấu hình. Khởi động lại Grafana để áp dụng." -ForegroundColor Green
