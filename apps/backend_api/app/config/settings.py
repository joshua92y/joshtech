# app/config/settings.py
from pydantic import BaseSettings


class Settings(BaseSettings):
    env: str = "prod"
    auth_verify_url: str = "http://admin.example.com/accounts/verify/"
    redis_url: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"


settings = Settings()
