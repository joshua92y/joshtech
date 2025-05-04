# 재현성을 위해 특정 마이너 버전 사용 권장
FROM python:3.11.5-slim

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 파이썬 관련 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE 1  # .pyc 파일 생성 방지
ENV PYTHONUNBUFFERED 1         # 파이썬 버퍼링 비활성화 (로그 확인 용이)

# 컨테이너 내부 작업 디렉토리 설정
WORKDIR /app

# 비루트 사용자 생성
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app -s /sbin/nologin -c "Docker image user" appuser

# requirements.txt 복사 및 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# === 애플리케이션 코드 복사 (권한 포함) ===
COPY --chown=appuser:appgroup apps/backend_api /app
COPY --chown=appuser:appgroup packages/shared_schemas /shared_schemas

# 비루트 사용자로 전환
USER appuser

# Railway는 PORT 환경 변수로 포트를 주입함
EXPOSE 8000

# PYTHONPATH 설정 (shared_schemas 참조 가능하게)
ENV PYTHONPATH="${PYTHONPATH}:/shared_schemas"

# FastAPI 앱 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
