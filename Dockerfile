# ./Dockerfile
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
ENV PYTHONUNBUFFERED 1       # 파이썬 버퍼링 비활성화 (로그 확인 용이)

# 컨테이너 내부 작업 디렉토리 설정
WORKDIR /app

# 보안을 위해 non-root 사용자 및 그룹 생성
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app -s /sbin/nologin -c "Docker image user" appuser

# === 의존성 설치 ===
# Docker 캐시를 활용하기 위해 requirements.txt 파일만 먼저 복사
# requirements.txt가 프로젝트 루트(빌드 컨텍스트)에 있다고 가정
COPY requirements.txt .

# 의존성 설치
# pip를 먼저 업그레이드하는 것이 좋음
# --no-cache-dir 옵션으로 레이어 크기 줄이기
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# === 애플리케이션 코드 복사 ===
# 백엔드 API에 필요한 특정 애플리케이션 코드만 복사
# 경로는 프로젝트 루트(빌드 컨텍스트) 기준
# FastAPI 코드 복사
COPY apps/backend_api /app
# shared-schemas 복사
COPY packages/shared_schemas /shared_schemas
# === 마무리 작업 ===
# /app 디렉토리 소유권을 non-root 사용자에게 변경
RUN chown -R appuser:appgroup /app

# non-root 사용자로 전환
USER appuser

# 앱이 리슨할 포트 명시 (문서화/메타데이터 목적)
# Railway는 PORT 환경 변수를 통해 실제 포트를 결정함
EXPOSE 8000

# PYTHONPATH 설정 추가
ENV PYTHONPATH="${PYTHONPATH}:/shared-schemas"

# shared-schemas도 소유권 변경
RUN chown -R appuser:appgroup /app /shared_schemas

# uvicorn으로 애플리케이션 실행
# Uvicorn은 Railway에 의해 PORT 환경 변수가 설정되면 자동으로 사용함.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]