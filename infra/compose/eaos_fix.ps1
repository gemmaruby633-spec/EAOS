# EAOS auto-fix script: backup + rename + restart compose
$ts = (Get-Date -Format yyyyMMdd_HHmmss)
$bk = "D:\eaos_backups\compose_$ts"
New-Item -ItemType Directory -Path $bk -Force | Out-Null

function Backup-Volume($volName, $fileName) {
    Write-Host "Backing up volume $volName..."
    docker run --rm -v ${volName}:/data -v "${bk}:/backup" alpine `
      sh -c "tar czf /backup/${fileName}_$ts.tgz -C /data . || true"
}

# Backup tất cả volume quan trọng
Backup-Volume "pgdata" "postgres_pgdata"
Backup-Volume "grafana_data" "grafana_data"
Backup-Volume "neo4j_data" "neo4j_data"
Backup-Volume "neo4j_logs" "neo4j_logs"
Backup-Volume "minio_data" "minio_data"
Backup-Volume "ollama_data" "ollama_data"
Backup-Volume "qdrant_data" "qdrant_data"

function Rename-Container($name) {
    $ids = docker ps -a --filter "name=$name" --format "{{.ID}}"
    $i = 0
    foreach ($id in $ids) {
        if ($id) {
            $newName = "$name-orphan-$ts-$i"
            Write-Host "Renaming $name ($id) -> $newName"
            docker rename $id $newName
            $i++
        }
    }
}

# Rename tất cả container gây conflict
Rename-Container "eaos-postgres"
Rename-Container "eaos-grafana"
Rename-Container "eaos-otel"
Rename-Container "eaos-ollama"
Rename-Container "eaos-minio"
Rename-Container "eaos-prometheus"
Rename-Container "eaos-neo4j"
Rename-Container "eaos-qdrant"
Rename-Container "eaos-redis"

# Khởi lại compose
cd D:\EAOS\infra\compose
docker-compose up -d --remove-orphans

# Kiểm tra trạng thái
docker-compose ps
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"
