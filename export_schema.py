# export_schema.py (루트에서 실행)
import os
import sys
import django
from django.core.serializers.json import DjangoJSONEncoder
from pathlib import Path
import json

# 경로 설정
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / "apps" / "backend-admin"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.apps import apps

def model_to_jsonschema(model):
    fields = {}
    for field in model._meta.fields:
        field_type = field.get_internal_type()
        if field_type in ("CharField", "TextField", "EmailField", "URLField"):
            ftype = "string"
        elif field_type in ("IntegerField", "BigIntegerField"):
            ftype = "integer"
        elif field_type == "BooleanField":
            ftype = "boolean"
        elif field_type in ("DateTimeField", "DateField"):
            ftype = "string"
        else:
            ftype = "string"

        fields[field.name] = {"type": ftype}

    return {
        "title": model.__name__,
        "type": "object",
        "properties": fields,
        "required": [f.name for f in model._meta.fields if not f.null and not f.blank]
    }

output_dir = BASE_DIR / "schemas"
output_dir.mkdir(exist_ok=True)

models = [
    apps.get_model("resume", "Resume"),
    apps.get_model("projects", "Project"),
    apps.get_model("contact", "ContactMessage"),
]

for model in models:
    schema = model_to_jsonschema(model)
    with open(output_dir / f"{model.__name__}.json", "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, cls=DjangoJSONEncoder)
