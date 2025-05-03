# apps/backend-admin/Dockerfile

FROM python:3.11-slim

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리
WORKDIR /app

# Django 프로젝트 복사
COPY apps/backend-admin /app

# shared-schemas 복사
COPY packages/shared-schemas /shared-schemas

# PYTHONPATH에 shared-schemas 추가
ENV PYTHONPATH="${PYTHONPATH}:/shared-schemas"

# 종속성 설치
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Django 서버 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]