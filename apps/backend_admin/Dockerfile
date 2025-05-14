#\apps\backend_admin\Dockerfile

# ✅ 베이스 이미지: Python 3.11.5의 슬림 버전 사용
FROM python:3.11.5-slim

# ✅ 시스템 패키지 설치 (PostgreSQL 연동 및 빌드 도구)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*  
# 이미지 용량 최소화

# ✅ Python 실행 환경 설정
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# .pyc 파일 생성 방지
# 출력 버퍼링 제거 (로그 실시간 출력)

# ✅ 컨테이너 작업 디렉토리 설정
WORKDIR /app

# ✅ 보안 강화를 위해 전용 사용자 추가
RUN groupadd -r appgroup && \
    useradd -r -g appgroup -d /app -s /sbin/nologin -c "Docker image user" appuser

# ✅ 의존성 설치 (프로젝트 루트 기준 경로로 COPY)
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ✅ 앱 코드 및 공통 스키마 복사 (Render는 항상 루트 기준으로 COPY)
COPY apps/backend_admin /app
COPY packages/shared_schemas /shared_schemas

# ✅ shared_schemas를 PYTHONPATH에 등록 (FastAPI에서도 참조 가능)
ENV PYTHONPATH="${PYTHONPATH}:/shared_schemas"

# ✅ staticfiles 디렉토리 생성 및 정적 파일 수집
RUN mkdir -p /app/staticfiles && \
    chown -R appuser:appgroup /app/staticfiles && \
    python manage.py collectstatic --noinput

# ✅ 루트 계정이 아닌 일반 사용자로 전환
USER appuser

# ✅ 문서화를 위한 포트 노출 (Render는 PORT 환경변수 자동 주입)
EXPOSE 8000

# ✅ Django 서버 실행 (이미 정적 파일이 수집되어 있으므로 collectstatic 제외)
CMD ["sh", "-c", "python manage.py migrate && uvicorn config.asgi:application --host 0.0.0.0 --port ${PORT:-8000}"]