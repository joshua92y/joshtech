# app/config/settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "prod"
    auth_verify_url: str = "http://admin.example.com/accounts/verify/"
    redis_url: str = "redis://localhost:6379"
    redis_host: str = "localhost"
    redis_port: int = 6379

    class Config:
        env_file = ".env"


settings = Settings()
