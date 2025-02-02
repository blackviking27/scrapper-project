from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    WEBSITE_DATA_URL: str
    COMPANY_DETAILS_URL: str
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()