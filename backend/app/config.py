from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Pydantic автоматически подтянет эти переменные из .env файла
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"  # Оптимальная по скорости и цене модель
    PORT: int = 8000
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
