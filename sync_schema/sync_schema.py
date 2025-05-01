import os
import sys
import django
import subprocess
import json
from pathlib import Path
from datetime import datetime
from django.apps import apps as django_apps

# 🔧 기본 경로 설정
BASE_DIR = Path(__file__).resolve().parents[1]
BACKEND_PATH = BASE_DIR / "apps" / "backend-admin"
SCHEMA_PATH = BASE_DIR / "schemas"
BACKUP_ROOT = SCHEMA_PATH / "backup"
SHARED_PATH = BASE_DIR / "packages" / "shared-schemas"

# Django 세팅 적용
sys.path.append(str(BACKEND_PATH))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# 📁 디렉토리 보장
SCHEMA_PATH.mkdir(parents=True, exist_ok=True)
SHARED_PATH.mkdir(parents=True, exist_ok=True)
BACKUP_ROOT.mkdir(parents=True, exist_ok=True)

# ✅ Django 기본 필드 타입 → JSON Schema 타입 매핑
TYPE_MAP = {
    "CharField": "string",
    "TextField": "string",
    "EmailField": "string",
    "URLField": "string",
    "IntegerField": "integer",
    "BigIntegerField": "integer",
    "BooleanField": "boolean",
    "DateField": "string",
    "DateTimeField": "string",
}

# ✅ 대상 앱 자동 필터링: backend-admin 하위만
PROJECT_APPS_BASE = str(BACKEND_PATH)
TARGET_APPS = [
    app_config.label
    for app_config in django_apps.get_app_configs()
    if PROJECT_APPS_BASE in str(app_config.path)
]

print(f"[🎯] 대상 앱 자동 감지됨: {TARGET_APPS}")

# 📦 백업 디렉토리 설정: schemas/backup/YYYYMMDD_01/
today = datetime.today().strftime("%Y%m%d")
existing = list((BACKUP_ROOT).glob(f"{today}_*"))
next_index = (
    max(
        [int(folder.name.split("_")[1]) for folder in existing if "_" in folder.name],
        default=0,
    )
    + 1
)
backup_dir = BACKUP_ROOT / f"{today}_{next_index:02}"
backup_dir.mkdir(parents=True, exist_ok=True)

print(f"[📦] 백업 디렉토리: {backup_dir}")

# 🔁 앱 내 모델 순회 및 처리
for model in django_apps.get_models():
    if model._meta.app_label not in TARGET_APPS:
        continue

    model_name = model.__name__
    fields = {
        f.name: {"type": TYPE_MAP.get(f.get_internal_type(), "string")}
        for f in model._meta.fields
    }
    schema = {
        "title": model_name,
        "type": "object",
        "properties": fields,
        "required": [f.name for f in model._meta.fields if not f.null and not f.blank],
    }

    # 📄 파일 경로
    json_file = SCHEMA_PATH / f"{model_name}.json"
    py_file = SHARED_PATH / f"{model_name}.py"
    backup_file = backup_dir / f"{model_name}.json"

    # 💾 JSON 저장 및 백업
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)
    with open(backup_file, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)

    # 🧬 Pydantic 모델 생성
    print(f"🔧 generating {py_file.name}...")
    subprocess.run(
        [
            "datamodel-codegen",
            "--input",
            str(json_file),
            "--input-file-type",
            "jsonschema",
            "--output",
            str(py_file),
        ]
    )
