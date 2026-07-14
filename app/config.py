# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database & cache
    DATABASE_URL: str
    REDIS_URL: str = ""

    # JWT (used in Phase 7)
    JWT_SECRET: str
    JWT_EXPIRE_MINUTES: int = 15

    # Frontend & OTP
    FRONTEND_URL: str = "http://localhost:5173"
    OTP_EXPIRE_SECONDS: int = 300
    OTP_DEV_MODE: bool = False

    # Launch features
    FEATURE_LOGIN_ENABLED: bool = False
    EARLY_BIRD_LIMIT: int = 50
    EARLY_BIRD_DISCOUNT_PERCENT: int = 25

    # Rate limits
    RATE_LIMIT_REGISTER_PER_IP: int = 5
    RATE_LIMIT_OTP_PER_IDENTIFIER: int = 3

    # SMS / email (optional in dev)
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_FROM_NUMBER: str = ""
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "noreply@baithak.pk"

settings = Settings()