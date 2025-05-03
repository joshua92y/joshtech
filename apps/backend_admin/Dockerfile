# apps/backend-admin/Dockerfile
# 재현성을 위해 특정 마이너 버전 고정
FROM python:3.11.5-slim

# 시스템 패키지 설치 (PostgreSQL 연동 및 C 확장 빌드용)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 파이썬 관련 환경 변수
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 설정
WORKDIR /app

# non-root 사용자 생성 (보안 강화)
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app -s /sbin/nologin -c "Docker image user" appuser

# requirements.txt만 먼저 복사해 캐시 최적화
COPY requirements.txt .

# 의존성 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Django 앱 복사
COPY apps/backend-admin /app

# shared-schemas 복사
COPY packages/shared-schemas /shared-schemas

# PYTHONPATH 설정: shared 모듈을 import 가능하게
ENV PYTHONPATH="${PYTHONPATH}:/shared-schemas"

# shared-schemas 권한도 함께 변경
RUN chown -R appuser:appgroup /app /shared-schemas

# non-root 사용자 전환
USER appuser

# 문서화를 위한 포트 노출 (실제 포트는 Render가 설정함)
EXPOSE 8000

# Django 서버 실행 (Render에서는 PORT 환경변수 자동 주입됨)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
