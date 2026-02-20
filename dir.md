# 📁 JoshuaTech — 프로젝트 디렉토리 구조

> 마지막 업데이트: 2026-02-20

---

## 개요

모노레포 구조의 풀스택 포트폴리오/블로그 플랫폼.  
Django 관리자 + FastAPI 백엔드 API + Next.js 프론트엔드 + Dragonfly Worker 구성.

---

```
joshuatech/
│
├── .github/workflows/                     # CI/CD 파이프라인
│   ├── deploy-django-ghcr.yml             #   Django 관리자 배포
│   ├── deploy-dragonfly-worker.yml        #   Dragonfly Worker 배포
│   ├── deploy-fastapi-ghcr.yml            #   FastAPI 배포
│   └── deploy-nextjs-ghcr.yml             #   Next.js 프론트엔드 배포
│
├── apps/                                  # 애플리케이션 모듈
│   │
│   ├── backend_admin/                     # 🐍 Django 관리자 백엔드
│   │   ├── Dockerfile
│   │   ├── manage.py
│   │   ├── requirements.txt
│   │   ├── config/                        #   Django 설정
│   │   │   ├── __init__.py
│   │   │   ├── asgi.py
│   │   │   ├── settings.py
│   │   │   ├── urls.py
│   │   │   └── wsgi.py
│   │   ├── accounts/                      #   사용자 인증/계정 관리
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── signals.py
│   │   │   ├── token.py
│   │   │   ├── urls.py
│   │   │   ├── views.py
│   │   │   ├── fastapi/
│   │   │   │   └── registerAPIView.py     #   FastAPI 회원가입 뷰
│   │   │   ├── utils/
│   │   │   │   └── auth.py                #   인증 유틸리티
│   │   │   └── migrations/
│   │   ├── contact/                       #   연락처/문의 관리
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   ├── views.py
│   │   │   └── migrations/
│   │   ├── content/                       #   마크다운 콘텐츠 관리
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   ├── views.py
│   │   │   └── migrations/
│   │   ├── projects/                      #   프로젝트 포트폴리오 관리
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   └── migrations/
│   │   ├── R2_Storage/                    #   Cloudflare R2 파일 스토리지
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   ├── views.py
│   │   │   └── migrations/
│   │   ├── resume/                        #   이력서 관리
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── forms.py
│   │   │   ├── models.py
│   │   │   ├── urls.py
│   │   │   ├── views.py
│   │   │   └── migrations/
│   │   └── utils/                         #   공용 유틸리티
│   │       ├── ping_flyio.py              #     Fly.io 헬스체크
│   │       └── scheduler.py               #     스케줄러
│   │
│   ├── backend_api/                       # ⚡ FastAPI 백엔드 API
│   │   ├── Dockerfile
│   │   ├── fly.toml                       #   Fly.io 배포 설정
│   │   ├── Procfile
│   │   ├── requirements.txt
│   │   ├── app/
│   │   │   ├── main.py                    #   FastAPI 엔트리포인트
│   │   │   ├── config/
│   │   │   │   └── settings.py            #   환경 설정
│   │   │   ├── decorators/
│   │   │   │   └── auth.py                #   인증 데코레이터
│   │   │   ├── deps/
│   │   │   │   ├── auth.py                #   인증 의존성
│   │   │   │   └── redis_client.py        #   Redis 클라이언트
│   │   │   ├── middleware/
│   │   │   │   └── auth_middleware.py      #   인증 미들웨어
│   │   │   ├── routers/                   #   API 라우터
│   │   │   │   ├── accounts.py            #     계정 API
│   │   │   │   ├── contactAPI.py          #     문의 API
│   │   │   │   ├── frontAPI.py            #     프론트엔드 API
│   │   │   │   ├── projectAPI.py          #     프로젝트 API
│   │   │   │   ├── R2_Storage.py          #     R2 스토리지 API
│   │   │   │   ├── resumeAPI.py           #     이력서 API
│   │   │   │   └── securityAPI.py         #     보안 API
│   │   │   └── utils/
│   │   │       ├── cache/
│   │   │       │   └── redis.py           #   Redis 캐시 유틸
│   │   │       ├── ping_render.py         #   Render 헬스체크
│   │   │       ├── scheduler.py           #   스케줄러
│   │   │       └── utils_postmark.py      #   이메일(Postmark) 유틸
│   │   └── tests/
│   │       ├── test_contact.py
│   │       ├── test_project.py
│   │       └── test_resume.py
│   │
│   ├── frontend/                          # ⚛️ Next.js 프론트엔드
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   ├── next.config.js
│   │   ├── tailwind.config.ts
│   │   ├── tsconfig.json
│   │   ├── wrangler.toml                  #   Cloudflare Workers 설정
│   │   ├── components.json                #   shadcn/ui 설정
│   │   ├── eslint.config.mjs
│   │   ├── postcss.config.mjs
│   │   ├── prettier.config.mjs
│   │   ├── public/                        #   정적 파일
│   │   │   ├── fonts/
│   │   │   │   └── Inter.ttf
│   │   │   ├── images/
│   │   │   │   ├── avatar.jpg
│   │   │   │   ├── gallery/               #     갤러리 이미지 (8장)
│   │   │   │   ├── og/
│   │   │   │   │   └── home.jpg           #     OG 이미지
│   │   │   │   └── projects/
│   │   │   │       └── project-01/        #     프로젝트 이미지/영상
│   │   │   └── trademark/                 #   로고/아이콘 SVG
│   │   ├── scripts/
│   │   │   ├── generate-wrangler-toml.js
│   │   │   └── wsl-build.js
│   │   ├── src/
│   │   │   ├── app/                       #   Next.js App Router 페이지
│   │   │   │   ├── layout.tsx             #     루트 레이아웃
│   │   │   │   ├── page.tsx               #     홈페이지
│   │   │   │   ├── not-found.tsx          #     404 페이지
│   │   │   │   ├── about/
│   │   │   │   │   └── page.tsx           #     소개 페이지
│   │   │   │   ├── blog/
│   │   │   │   │   ├── page.tsx           #     블로그 목록
│   │   │   │   │   ├── [slug]/page.tsx    #     블로그 상세
│   │   │   │   │   └── posts/             #     MDX 블로그 글 (11개)
│   │   │   │   ├── gallery/
│   │   │   │   │   └── page.tsx           #     갤러리 페이지
│   │   │   │   ├── work/
│   │   │   │   │   ├── page.tsx           #     작업물 목록
│   │   │   │   │   ├── [slug]/page.tsx    #     작업물 상세
│   │   │   │   │   └── projects/          #     MDX 프로젝트 글 (3개)
│   │   │   │   ├── resources/             #     사이트 설정/콘텐츠 리소스
│   │   │   │   │   ├── config.js
│   │   │   │   │   ├── content.js
│   │   │   │   │   └── index.ts
│   │   │   │   ├── utils/
│   │   │   │   │   ├── formatDate.ts
│   │   │   │   │   └── utils.ts
│   │   │   │   └── og/
│   │   │   │       └── route.tsx.txt      #   OG 이미지 생성 (비활성)
│   │   │   ├── components/                #   커스텀 컴포넌트
│   │   │   │   ├── index.ts
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   ├── mdx.tsx
│   │   │   │   ├── RouteGuard.tsx
│   │   │   │   ├── ScrollToHash.tsx
│   │   │   │   ├── ThemeToggle.tsx
│   │   │   │   ├── Mailchimp.tsx
│   │   │   │   ├── HeadingLink.tsx
│   │   │   │   ├── ProjectCard.tsx
│   │   │   │   ├── about/
│   │   │   │   │   └── TableOfContents.tsx
│   │   │   │   ├── blog/
│   │   │   │   │   ├── Post.tsx
│   │   │   │   │   └── Posts.tsx
│   │   │   │   ├── gallery/
│   │   │   │   │   └── MasonryGrid.tsx
│   │   │   │   └── work/
│   │   │   │       └── Projects.tsx
│   │   │   ├── hooks/
│   │   │   │   └── useClientPathTracker.ts
│   │   │   ├── lib/
│   │   │   │   └── utils.ts
│   │   │   └── once-ui/                   #   Once UI 디자인 시스템
│   │   │       ├── components/            #     60+ UI 컴포넌트
│   │   │       ├── hooks/
│   │   │       ├── icons.ts
│   │   │       ├── interfaces.ts
│   │   │       ├── types.ts
│   │   │       ├── modules/
│   │   │       │   ├── code/              #     코드 하이라이팅
│   │   │       │   └── seo/               #     SEO (Meta, Schema)
│   │   │       ├── styles/                #     SCSS 스타일 토큰
│   │   │       └── tokens/                #     디자인 토큰
│   │   ├── static_assets/                 #   정적 에셋
│   │   └── types/
│   │       └── tailwindcss-fluid-type.d.ts
│   │
│   ├── worker/                            # 🔄 Dragonfly(Redis) 큐 워커
│   │   ├── Dockerfile.worker
│   │   ├── r2_worker.py                   #   R2 파일 업로드 워커
│   │   └── requirements.txt
│   │
│   └── test/                              # 🧪 통합 테스트
│       ├── admin/
│       │   ├── contact_save_date.http
│       │   └── contact_validate.http
│       └── api/
│           ├── contact_validate.http
│           ├── r2_upload.html
│           └── r2_upload.http
│
├── packages/                              # 📦 공유 패키지
│   ├── shared_queue/                      #   Redis 큐 공유 모듈
│   │   └── redis_queue.py
│   └── shared_schemas/                    #   Pydantic/공유 스키마
│       ├── BlacklistedToken.py
│       ├── Contactmessage.py
│       ├── ContentType.py
│       ├── FileMeta.py
│       ├── Group.py
│       ├── LogEntry.py
│       ├── MarkdownPost.py
│       ├── OutstandingToken.py
│       ├── Permission.py
│       ├── Project.py
│       ├── Resume.py
│       ├── Role.py
│       ├── Session.py
│       ├── User.py
│       └── UserDeviceToken.py
│
├── schemas/                               # 📋 JSON 스키마 정의
│   ├── BlacklistedToken.json
│   ├── ContactMessage.json
│   ├── ContentType.json
│   ├── FileMeta.json
│   ├── Group.json
│   ├── LogEntry.json
│   ├── MarkdownPost.json
│   ├── OutstandingToken.json
│   ├── Permission.json
│   ├── Project.json
│   ├── Resume.json
│   ├── Role.json
│   ├── Session.json
│   ├── User.json
│   ├── UserDeviceToken.json
│   └── backup/                            #   스키마 백업 이력
│       ├── 20250521_01/
│       ├── 20250527_01/
│       ├── 20250527_02/
│       ├── 20250527_03/
│       └── 20250527_04/
│
├── sync_schema/                           # 🔄 스키마 동기화 도구
│   ├── sync_schema.py
│   ├── sync-schema.bat
│   └── sync-schema.sh
│
├── infra/                                 # 🏗️ 인프라 설정
│   └── oci/                               #   Oracle Cloud Infrastructure
│       ├── docker-compose.yml             #     메인 서비스 Compose
│       ├── dragonfly-worker-compose.yml   #     워커 Compose
│       └── traefik/                       #     Traefik 리버스 프록시
│           ├── traefik.yml                #       정적 설정
│           ├── traefik_dynamic.yml        #       동적 설정
│           └── acme.json                  #       SSL 인증서
│
├── .github/workflows/                     # GitHub Actions CI/CD
├── .dockerignore
├── .eslintignore
├── .eslintrc.json
├── .gitignore
├── .prettierignore
├── .prettierrc.json
├── render.yaml                            # Render 배포 설정
├── requirements.txt                       # 루트 Python 의존성
├── package-lock.json                      # 루트 npm lockfile
├── README.md
└── dir.md                                 # (본 문서)
```

---

## 기술 스택 요약

| 영역 | 기술 |
|------|------|
| **프론트엔드** | Next.js, TypeScript, Tailwind CSS, Once UI, MDX |
| **백엔드 (Admin)** | Django, Django REST Framework |
| **백엔드 (API)** | FastAPI, Pydantic |
| **큐/워커** | Dragonfly (Redis 호환), Python Worker |
| **스토리지** | Cloudflare R2 |
| **인프라** | OCI, Docker, Traefik, Fly.io |
| **CI/CD** | GitHub Actions, GHCR |
| **이메일** | Postmark |

---

## 주요 모듈 설명

### `apps/backend_admin` — Django 관리자
Django 기반 관리 백엔드. 사용자 인증, 콘텐츠/프로젝트/이력서/파일 CRUD, 연락처 관리 등을 담당.

### `apps/backend_api` — FastAPI API 서버
클라이언트(프론트엔드)가 직접 호출하는 REST API. Redis 캐싱, JWT 인증, Postmark 이메일 전송 지원.

### `apps/frontend` — Next.js 포트폴리오 사이트
App Router 기반 SSR/SSG 포트폴리오·블로그. Once UI 디자인 시스템과 MDX 콘텐츠로 구성.

### `apps/worker` — R2 큐 워커
Dragonfly(Redis) 큐에서 작업을 수신하여 Cloudflare R2에 파일을 업로드하는 백그라운드 워커.

### `packages/` — 공유 패키지
- **shared_queue**: Redis 큐 발행/소비 공유 로직
- **shared_schemas**: Django ↔ FastAPI 간 공유되는 Pydantic 모델

### `schemas/` — JSON 스키마
Django 모델에서 추출한 JSON Schema 정의 파일. `sync_schema/`를 통해 자동 동기화.

### `infra/oci/` — OCI 인프라
Oracle Cloud에서 Docker Compose + Traefik으로 서비스를 운영하기 위한 설정.