# app/config/settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "prod"
    auth_verify_url: str = "http://admin.joshuatech.dev/accounts/verify/"
    redis_url: str = "redis://158.180.87.55:6379"
    redis_host: str = "158.180.87.55"
    redis_port: int = 6379
    redis_password: str | None = None  # 설정 시 추가

    class Config:
        env_file = ".env"


settings = Settings()
