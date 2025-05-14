# apps/backend_api/Dockerfile

# ✅ Python 3.11.5 슬림 베이스 이미지
FROM python:3.11.5-slim

# ✅ 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ✅ 파이썬 실행 환경 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# ✅ 작업 디렉토리 지정
WORKDIR /app

# ✅ 전용 사용자 추가 (보안 강화)
RUN groupadd -r appgroup && \
    useradd -r -g appgroup -d /app -s /sbin/nologin -c "Docker image user" appuser

# ✅ requirements.txt만 복사 (캐시 최적화)
COPY requirements.txt .

# ✅ 패키지 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir "pydantic[email]"

# ✅ 앱 코드 및 공용 스키마 복사 (루트 기준)
COPY apps/backend_api /app
COPY packages/shared_schemas /shared_schemas

# ✅ PYTHONPATH 설정
ENV PYTHONPATH="${PYTHONPATH}:/shared_schemas"

# ✅ 비루트 사용자로 전환
USER appuser

# ✅ 포트 지정 (PORT 자동 주입)
EXPOSE 8000

# ✅ FastAPI 서버 실행
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]