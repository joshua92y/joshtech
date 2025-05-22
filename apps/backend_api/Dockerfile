# ✅ 1. Python 슬림 이미지 사용 (빌드 속도/용량 최적화)
FROM python:3.11-slim

# ✅ 2. 필수 시스템 패키지 설치 (no-recommends로 경량화)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
    chromium \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# ✅ 3. Chromium 경로 통일
RUN [ "$(which chromium || which chromium-browser)" != "/usr/bin/chromium" ] && \
    ln -sf $(which chromium || which chromium-browser) /usr/bin/chromium || true

# ✅ 4. 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HTI_BROWSER_PATH=/usr/bin/chromium

# ✅ 5. 작업 디렉토리 및 사용자 생성
WORKDIR /app
RUN groupadd -r appgroup && \
    useradd -r -g appgroup -d /app -s /sbin/nologin -c "Docker image user" appuser

# ✅ 6. requirements.txt만 복사 → 캐시 최적화
COPY requirements.txt .

# ✅ 7. pip 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir "pydantic[email]"

# ✅ 8. 앱 코드 및 공용 스키마 복사
COPY apps/backend_api /app
COPY packages/shared_schemas /shared_schemas
COPY packages/shared_queue /shared_queue

# ✅ 9. PYTHONPATH 설정
ENV PYTHONPATH="${PYTHONPATH}:/shared_schemas"
ENV PYTHONPATH="${PYTHONPATH}:/shared_queue"
# ✅ 10. 비루트 사용자 전환
USER appuser

# ✅ 11. 포트 및 실행 명령
EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
