# apps\backend_admin\config\settings.py
from pathlib import Path
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from datetime import timedelta

# 🟡 환경 변수 로드
load_dotenv()

# 📁 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 보안 설정
SECRET_KEY = "django-insecure-khmm$7h-h3@bltm#vz=*_n(74)y_s2dy&zkyjfiwpf^y#br3v!"
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost").split(",")

# 🌐 CORS/CSRF 설정
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_HEADERS = [
    "authorization",
    "content-type",
    "x-csrftoken",
]
CORS_ALLOW_ALL_ORIGINS = DEBUG
if not DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "https://joshuatech.dev",
        "https://www.joshuatech.dev",
    ]
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "https://mainapi.joshuatech.dev,http://127.0.0.1:8000",
).split(",")

# 🧩 모델 설정
AUTH_USER_MODEL = "accounts.User"

# 🧩 앱 정의
INSTALLED_APPS = [
    # Admin UI 개선
    "jazzmin",
    # Django 기본 앱
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 사용자 앱
    "resume",
    "projects",
    "contact",
    "accounts",
    # DRF 및 인증
    "rest_framework",
    "rest_framework_simplejwt",  # ✅ 추가 권장
    "rest_framework_simplejwt.token_blacklist",
    # 기타 유틸
    "corsheaders",
    "R2_Storage",
    # 선택적 기능
    "drf_spectacular",
    "drf_spectacular_sidecar",  # Swagger/OpenAPI 문서용
    # "taggit",  # 태그 기능
    # "storages",  # S3, R2 연동
]
# 🧱 미들웨어
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
# REST_FRAMEWORK 설정
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# 🌐 URL 설정
ROOT_URLCONF = "config.urls"

# 🖼 템플릿
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# 🔥 WSGI
WSGI_APPLICATION = "config.wsgi.application"

# 🗄 DB 설정 (PostgreSQL)
if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    tmpPostgres = urlparse(os.getenv("DATABASE_URL"))
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": tmpPostgres.path[1:],
            "USER": tmpPostgres.username,
            "PASSWORD": tmpPostgres.password,
            "HOST": tmpPostgres.hostname,
            "PORT": tmpPostgres.port or 5432,
        }
    }

# 🔐 비밀번호 검증
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# JWT 설정
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_BLACKLIST_ENABLED": True,
}
INTERNAL_API_KEY = os.getenv(
    "INTERNAL_API_KEY",
    "a601d47cad3a512c79ed67c44f396dbc330263f2d125a8fc32a978233acf4a0b",
)
MAX_DEVICE_COUNT = int(os.getenv("MAX_DEVICE_COUNT", 3))

FASTAPI_CACHE_INVALIDATE_URL = os.getenv(
    "FASTAPI_CACHE_INVALIDATE_URL",
    "https://api.joshuatech.dev/internal/cache-invalidate-role/",
)
# 🌍 국제화
LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

# 📁 정적/미디어 파일
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# 🔑 기본 키 설정
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 🟪 Sentry 설정은 마지막에!
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://b1e56428d1ce88d73ef17fb8aade5d5e@o4509302473621504.ingest.us.sentry.io/4509302475259904",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
    environment="prod",
)
