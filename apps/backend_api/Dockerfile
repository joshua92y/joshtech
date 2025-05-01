# apps/backend_api/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY ./app /app/app
COPY ./tests /app/tests
COPY ../../packages/shared_schemas /app/packages/shared_schemas
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
