from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_USERNAME: Optional[str] = None
    DATABASE_PASSWORD: Optional[str] = None
    DATABASE_HOST: Optional[str] = None
    DATABASE_PORT: Optional[str] = None
    DATABASE_NAME: Optional[str] = None
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    ENV:str="dev"
    SENTRY_DSN:str=None
    REFRESH_SECRET_KEY:str
    REFRESH_TOKEN_EXPIRE_DAYS:int

    class Config:
        env_file="dotenv"

settings = Settings()