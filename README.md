# JoshuaTech — 포트폴리오 프로젝트 제안서

**Joshua | Full-Stack Developer | 2025**

---

## 프로젝트 개요

개인 포트폴리오 및 블로그 플랫폼을 처음부터 직접 설계·구축·운영한 풀스택 프로젝트.
단순 토이 프로젝트가 아닌, **실 서비스 운영을 전제로 한 프로덕션 수준의 모노레포**.

| 항목 | 내용 |
|------|------|
| 개발 기간 | 약 1개월 (기획 → 설계 → 구현 → 배포 1인 전담) |
| 서비스 형태 | 개인 포트폴리오 / 블로그 |
| API 평균 응답 | 1.5초 이내 |
| 업타임 | 99% |

---

## 아키텍처

```
Next.js (Frontend)
    ↓ REST API
FastAPI (API Server)  ←→  Redis (Dragonfly)  ←→  Worker
    ↓ Auth 위임
Django Admin (DB 관리)
    ↓
PostgreSQL  +  Cloudflare R2 (파일 스토리지)
```

**인프라**: OCI VM + Docker Compose + Traefik (리버스 프록시) + GitHub Actions CI/CD

---

## 핵심 기술 결정 3가지

### 1. Django + FastAPI 역할 분리

단일 프레임워크 대신 두 백엔드를 목적별로 분리.

- **Django Admin** — ORM, 마이그레이션, 관리자 UI 등 DB 직접 관리가 필요한 영역
- **FastAPI** — 프론트엔드가 호출하는 기능 단위 API, MSA 구조로 독립 배포

→ 각 프레임워크의 강점만 취하고 결합도를 최소화

### 2. Redis 대신 Dragonfly 선택

파일 삭제 큐(worker) 및 JWT 캐시에 Redis 호환 큐 사용.
Dragonfly는 Redis 대비 멀티스레드 구조로 처리 성능이 우수하며,
동일한 Redis 프로토콜을 사용하므로 코드 변경 없이 전환 가능.

### 3. OCI 직접 운영 (Managed 서비스 대신)

Vercel / Render 같은 플랫폼 대신 OCI Free Tier VM 기반 직접 운영 선택.

- 향후 지오코딩, 지도 기반 기능 확장을 고려한 컴퓨팅 유연성 확보
- Free Tier 기준 성능 대비 비용 효율이 가장 우수
- Traefik으로 SSL 자동화 및 라우팅 직접 제어

---

## 문제 해결 사례

**문제**: GitHub Actions 빌드·배포 시간이 15분 이상 소요 → 개발 사이클이 느려짐

**원인 분석**: Docker 이미지 레이어 캐시 미적용, 단일 아키텍처 빌드

**해결**:
- GHA 캐시(`type=gha`) + BuildKit 레이어 캐시 전략 재구성
- multi-arch(`linux/amd64, arm64`) 빌드 병렬화
- 경로 기반 트리거로 변경된 앱만 빌드 (`paths:` 필터)

**결과**: 빌드 시간 **15분 → 10분** (약 33% 단축)

---

## 기술 스택

| 영역 | 기술 |
|------|------|
| Frontend | Next.js, TypeScript, Tailwind CSS, MDX |
| Backend API | FastAPI, Pydantic |
| Backend Admin | Django, Django REST Framework |
| Queue / Worker | Dragonfly, Python async worker |
| Storage | Cloudflare R2 (S3 호환) |
| Infra | OCI, Docker, Traefik |
| CI/CD | GitHub Actions, GHCR (멀티 아키텍처) |
