# ✅ 베이스 이미지: Python 3.11.5의 슬림 버전 사용 (최신 보안 패치 + 가벼움)
FROM python:3.11.5-slim

# ✅ 시스템 패키지 설치
# - PostgreSQL 연동: libpq-dev
# - Python C 확장 빌드를 위한 도구들: gcc, build-essential
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*  # 캐시 제거로 이미지 크기 최소화

# ✅ Python 실행 환경 설정
ENV PYTHONDONTWRITEBYTECODE 1  # .pyc 파일 생성 방지
ENV PYTHONUNBUFFERED 1         # stdout/stderr 버퍼링 비활성화 (로그 실시간 출력)

# ✅ 컨테이너 내 작업 디렉토리 설정
WORKDIR /app

# ✅ 보안을 위해 루트가 아닌 전용 사용자 생성
RUN groupadd -r appgroup && \
    useradd -r -g appgroup -d /app -s /sbin/nologin -c "Docker image user" appuser

# ✅ 의존성 설치를 위한 requirements.txt 복사
COPY requirements.txt .

# ✅ pip 업그레이드 후 requirements 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ✅ Django 앱 복사 (소유권 지정)
COPY --chown=appuser:appgroup apps/backend_admin /app

# ✅ 공유 Pydantic 스키마 복사 (소유권 지정)
COPY --chown=appuser:appgroup packages/shared_schemas /shared_schemas

# ✅ PYTHONPATH 등록: FastAPI와 Django 양쪽에서 shared_schemas 모듈 인식 가능하게
ENV PYTHONPATH="${PYTHONPATH}:/shared_schemas"

# ❌ 이전 방식: 소유권 변경 명령 (Render 환경에서 권한 오류 발생 가능)
# RUN chown -R appuser:appgroup /app /shared_schemas

# ✅ 비루트 사용자로 전환 (보안 강화)
USER appuser

# ✅ 문서화를 위한 포트 노출 (실제 사용되는 포트는 Render가 PORT 환경변수로 주입)
EXPOSE 8000

# ✅ Django 개발 서버 실행 명령 (Render는 PORT 환경변수 자동 전달)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
