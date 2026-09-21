from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    GOOGLE_MAPS_API_KEY: str
    SECRET_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings()