# ✅ 베이스 이미지: Python 3.11.5의 슬림 버전 사용
FROM python:3.11.5-slim

# ✅ 시스템 패키지 설치 (PostgreSQL 연동 및 빌드 도구)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*  

# ✅ Python 실행 환경 설정
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ✅ 컨테이너 작업 디렉토리 설정
WORKDIR /app

# ✅ 보안 강화를 위해 전용 사용자 추가
RUN groupadd -r appgroup && \
    useradd -r -g appgroup -d /app -s /sbin/nologin -c "Docker image user" appuser

# ✅ 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ✅ 앱 코드 및 공통 스키마 복사
COPY apps/backend_admin /app
COPY packages/shared_schemas /shared_schemas
COPY packages/shared_queue /shared_queue

# ✅ shared_schemas와 shared_queue를 PYTHONPATH에 등록
ENV PYTHONPATH="${PYTHONPATH}:/shared_schemas"
ENV PYTHONPATH="${PYTHONPATH}:/shared_queue"

# ✅ staticfiles 디렉토리 생성
RUN mkdir -p /app/staticfiles && \
    chown -R appuser:appgroup /app/staticfiles

# ✅ 루트 계정이 아닌 일반 사용자로 전환
USER appuser

# ✅ 문서화를 위한 포트 노출 (Render는 PORT 환경변수 자동 주입)
EXPOSE 8000

# ✅ Django 서버 실행 
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && uvicorn config.asgi:application --host 0.0.0.0 --port ${PORT:-8000}"]

