#!/bin/bash
cd "$(dirname "$0")"  # 스크립트 디렉토리로 이동
set -e

echo "[1/3] 🔄 makemigrations..."
python ../apps/backend_admin/manage.py makemigrations

echo "[2/3] 🗃️ migrate..."
python ../apps/backend_admin/manage.py migrate

echo "[3/3] 🧬 export + generate Pydantic models..."
python sync_schema.py

echo "✅ 완료!"