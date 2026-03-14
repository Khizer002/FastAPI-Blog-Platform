from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from .config import settings

# 1. Try to get the full URL first (Railway's default)
DATABASE_URL = os.getenv("MYSQL_URL")

if DATABASE_URL:
    # Handle the driver prefix for SQLAlchemy
    if DATABASE_URL.startswith("mysql://"):
        SQLALCHEMY_DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+mysqlconnector://", 1)
    else:
        SQLALCHEMY_DATABASE_URL = DATABASE_URL
else:
    # 2. Local development fallback
    # Use .get() with a default '3306' to prevent the 'None' int conversion error
    user = settings.DATABASE_USERNAME
    password = settings.DATABASE_PASSWORD
    host = settings.DATABASE_HOST
    port = settings.DATABASE_PORT if settings.DATABASE_PORT else "3306"
    db_name = settings.DATABASE_NAME
    
    SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db_name}"

# 3. Create the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()