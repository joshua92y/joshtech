FROM python:3.11-slim

WORKDIR /app

COPY ./app /app/app
COPY ./packages /app/packages
COPY requirements.txt .

# 필수 빌드 툴 설치 (슬림 이미지일 경우)
RUN apt-get update && apt-get install -y gcc libpq-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y gcc libpq-dev && apt-get autoremove -y

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
