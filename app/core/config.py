from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    model_name: str = "ProsusAI/finbert"
    database_url: str = "sqlite:///./sentiment.db"
    max_text_length: int = 5000


settings = Settings()
