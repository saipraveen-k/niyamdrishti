"""
Application configuration using Pydantic Settings.
All values are loaded from environment variables or .env file.
"""

from functools import lru_cache
from typing import List, Literal, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "NiyamDrishti"
    app_env: Literal["development", "staging", "production"] = "development"
    debug: bool = False
    secret_key: str = Field(min_length=32)
    frontend_url: str = "http://localhost:3000"
    allowed_origins: str = "http://localhost:3000"

    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str

    # Database
    database_url: str
    database_url_sync: Optional[str] = None

    # AI
    ai_provider: Literal["openai", "anthropic"] = "openai"
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    openai_extraction_model: str = "gpt-4o"
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-5-haiku-20241022"
    anthropic_extraction_model: str = "claude-3-5-sonnet-20241022"

    # Document processing
    max_upload_size_bytes: int = 20 * 1024 * 1024  # 20 MB
    max_pdf_pages: int = 200
    tesseract_cmd: Optional[str] = None
    ocr_min_confidence: int = 60

    # Storage buckets
    official_docs_bucket: str = "official-documents"
    student_uploads_bucket: str = "student-uploads"
    reports_bucket: str = "generated-reports"
    signed_url_expiry: int = 3600  # 1 hour

    # Document retention
    student_doc_retention_days: int = 30

    # Authentication
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30
    login_max_attempts: int = 5
    login_attempt_window_minutes: int = 15

    # Email
    email_provider: str = "supabase_smtp"
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    from_email: str = "noreply@niyamdrishti.in"
    from_name: str = "NiyamDrishti"

    # Logging
    log_level: str = "INFO"
    log_format: Literal["json", "console"] = "console"

    # Worker
    worker_poll_interval: int = 5
    worker_max_retries: int = 3
    worker_retry_backoff_seconds: int = 60

    @field_validator("allowed_origins")
    @classmethod
    def parse_origins(cls, v: str) -> str:
        # Keep as string; conversion to list in property
        return v

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"

    @property
    def ai_available(self) -> bool:
        if self.ai_provider == "openai":
            return bool(self.openai_api_key)
        elif self.ai_provider == "anthropic":
            return bool(self.anthropic_api_key)
        return False


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance. Import and call this everywhere."""
    return Settings()


settings = get_settings()
