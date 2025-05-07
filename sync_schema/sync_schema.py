import os
import sys
import django
import subprocess
import json
from pathlib import Path
from datetime import datetime
from django.apps import apps as django_apps

# 📁 경로 설정
CURRENT_DIR = Path(__file__).resolve()
BASE_DIR = CURRENT_DIR.parents[1]
BACKEND_PATH = BASE_DIR / "apps"
BACKEND_ADMIN_PATH = BACKEND_PATH / "backend_admin"
SCHEMA_PATH = BASE_DIR / "schemas"
SHARED_PATH = BASE_DIR / "packages" / "shared_schemas"
BACKUP_ROOT = SCHEMA_PATH / "backup"

# Django 환경 설정
sys.path.append(str(BACKEND_PATH))
sys.path.append(str(BACKEND_ADMIN_PATH))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# 📁 디렉토리 생성
SCHEMA_PATH.mkdir(parents=True, exist_ok=True)
SHARED_PATH.mkdir(parents=True, exist_ok=True)
BACKUP_ROOT.mkdir(parents=True, exist_ok=True)

# Django 필드 타입 → JSON 타입 매핑
TYPE_MAP = {
    "AutoField": "integer",
    "BigAutoField": "integer",
    "BigIntegerField": "integer",
    "BinaryField": "string",
    "BooleanField": "boolean",
    "CharField": "string",
    "DateField": "string",
    "DateTimeField": "string",
    "DecimalField": "number",
    "DurationField": "string",
    "EmailField": "string",
    "FileField": "string",
    "FilePathField": "string",
    "FloatField": "number",
    "ImageField": "string",
    "IntegerField": "integer",
    "GenericIPAddressField": "string",
    "JSONField": "object",
    "NullBooleanField": "boolean",
    "PositiveIntegerField": "integer",
    "PositiveSmallIntegerField": "integer",
    "SlugField": "string",
    "SmallAutoField": "integer",
    "SmallIntegerField": "integer",
    "TextField": "string",
    "TimeField": "string",
    "URLField": "string",
    "UUIDField": "string",
    "ForeignKey": "integer",
    "OneToOneField": "integer",
    "ManyToManyField": "array",
}

# 대상 앱 필터링
PROJECT_APPS_BASE = str(BACKEND_PATH)
TARGET_APPS = [
    app.label
    for app in django_apps.get_app_configs()
    if PROJECT_APPS_BASE in str(app.path)
]
print(f"[🎯] 대상 앱 자동 감지됨: {TARGET_APPS}")

# 백업 디렉토리 생성
today = datetime.today().strftime("%Y%m%d")
existing = list(BACKUP_ROOT.glob(f"{today}_*"))
next_index = (
    max([int(folder.name.split("_")[1]) for folder in existing if "_" in folder.name], default=0) + 1
)
backup_dir = BACKUP_ROOT / f"{today}_{next_index:02}"
backup_dir.mkdir(parents=True, exist_ok=True)
print(f"[📦] 백업 디렉토리: {backup_dir}")

# 모델 순회
for model in django_apps.get_models():
    if model._meta.app_label not in TARGET_APPS:
        continue

    model_name = model.__name__
    fields = {}
    required = []

    for f in model._meta.fields:
        internal_type = f.get_internal_type()

        if internal_type not in TYPE_MAP:
            print(f"[⚠️] 타입 매핑 누락: {model_name}.{f.name} ({internal_type})")

        json_type = TYPE_MAP.get(internal_type, "string")
        field_schema = {
            "type": json_type,
            "title": f.verbose_name or f.name
        }

        # 날짜/시간 포맷
        if internal_type in ["DateTimeField", "DateField", "TimeField"]:
            field_schema["format"] = {
                "DateTimeField": "date-time",
                "DateField": "date",
                "TimeField": "time"
            }[internal_type]

        # choices → enum
        if f.choices:
            field_schema["enum"] = [choice[0] for choice in f.choices]

        # default
        if f.has_default() and f.default is not None:
            try:
                field_schema["default"] = f.get_default()
            except Exception:
                pass

        # nullable
        if f.null:
            field_schema["nullable"] = True

        fields[f.name] = field_schema

        # 필수 필드 판단
        if not f.null and not f.blank and not getattr(f, "auto_now", False) and not getattr(f, "auto_now_add", False):
            required.append(f.name)

    schema = {
        "title": model_name,
        "type": "object",
        "properties": fields,
        "required": required,
    }

    # 파일 저장
    json_file = SCHEMA_PATH / f"{model_name}.json"
    py_file = SHARED_PATH / f"{model_name}.py"
    backup_file = backup_dir / f"{model_name}.json"

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)
    with open(backup_file, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)

    print(f"🔧 generating {py_file.name}...")
    subprocess.run(
        [
            sys.executable, "-m", "datamodel_code_generator",
            "--input", str(json_file),
            "--input-file-type", "jsonschema",
            "--output", str(py_file),
            "--use-default",
            "--field-constraints",
            "--use-title-as-name"
        ]
    )
