# apps/backend_admin/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . /app
COPY ../../packages/shared_schemas /app/packages/shared_schemas

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
