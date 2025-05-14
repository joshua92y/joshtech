my-portfolio/
├── apps/
│   ├── frontend/               # Cloudflare Pages용 프론트 (React/Next.js)
│   │   ├── public/
│   │   ├── src/
│   │   ├── .env
│   │   └── package.json
│   │
│   ├── backend-admin/          # Django 백오피스 + 모델 정의
│   │   ├── config/             # Django 설정
│   │   ├── core/               # 공통 유틸
│   │   ├── resume/             # 이력서 관리용 앱
│   │   ├── projects/           # 프로젝트 관리용 앱
│   │   ├── contact/            # 컨택 메시지 관리 앱
│   │   ├── media/              # 업로드된 이력서 파일 저장
│   │   ├── manage.py
│   │   └── requirements.txt
│   │
│   └── backend-api/            # FastAPI API 서버
│       ├── app/
│       │   ├── main.py         # FastAPI 엔트리포인트
│       │   ├── api/            # 라우터 모듈
│       │   ├── db/             # DB 접속 (SQLAlchemy or Django 연동)
│       │   ├── models/         # SQLAlchemy 모델 or Pydantic 스키마
│       │   └── services/       # DB 쿼리 / 유즈케이스
│       ├── tests/
│       ├── .env
│       └── requirements.txt
│
├── packages/
│   └── shared-schemas/         # 공통 타입 정의 (Pydantic 기반 DTO)
│       ├── resume.py
│       ├── projects.py
│       └── contact.py
│
├── docker-compose.yml          # 로컬 개발용 서비스 통합
├── .gitignore
├── README.md
└── .env                        # 루트 공통 환경 변수 (DB URL 등)