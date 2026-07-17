from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent



class Settings(BaseSettings):
    AI_MODEL: str
    AI_KEY: str
    DATABASE_URL: str
    BASE_API_AI:str
    SMTP_USER: str
    ADMIN_EMAIL: str
    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_PASSWORD: str
    AI_SYSTEM_PROMPT: str
    SMTP_SENDER_EMAIL: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding='utf-8')


settings = Settings()
