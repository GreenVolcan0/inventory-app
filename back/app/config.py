from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str
    JWT_KEY: str
    JWT_ALG: str = "HS256"
    INITIAL_ADMIN_LOGIN: str
    INITIAL_ADMIN_PASSWORD: str
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRES_DAYS: int = 30

settings = Settings()