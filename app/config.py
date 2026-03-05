from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_USERNAME:str
    DATABASE_PASSWORD:str
    DATABASE_HOST:str
    DATABASE_PORT:str
    DATABASE_NAME:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int

    class Config:
        env_file="dotenv"

settings = Settings()