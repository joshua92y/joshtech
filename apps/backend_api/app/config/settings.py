# app/config/settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "prod"
    auth_verify_url: str = "http://admin.example.com/accounts/verify/"
    redis_url: str = "redis://129.154.49.74:6379"
    redis_host: str = "129.154.49.74"
    redis_port: int = 6379
    redis_password: str | None = None  # 설정 시 추가

    class Config:
        env_file = ".env"


settings = Settings()
