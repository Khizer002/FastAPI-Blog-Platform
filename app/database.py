from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from .config import settings
from loguru import logger

# 1. Try to get the full URL first (Railway's default)
DATABASE_URL = os.getenv("MYSQL_URL")

if DATABASE_URL:
    # Handle the driver prefix for SQLAlchemy
    if DATABASE_URL.startswith("mysql://"):
        SQLALCHEMY_DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+mysqlconnector://", 1)
        logger.info(f"Connecting to cloud database: {SQLALCHEMY_DATABASE_URL.split("@")[-1]} ")
    else:
        SQLALCHEMY_DATABASE_URL = DATABASE_URL
        logger.info(f"Connecting to cloud database: {SQLALCHEMY_DATABASE_URL.split("@")[-1]} ")
else:
    # 2. Local development fallback
    # Use .get() with a default '3306' to prevent the 'None' int conversion error
    user = settings.DATABASE_USERNAME
    password = settings.DATABASE_PASSWORD
    host = settings.DATABASE_HOST
    port = settings.DATABASE_PORT if settings.DATABASE_PORT else "3306"
    db_name = settings.DATABASE_NAME
    
    SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db_name}"
    logger.info(f"Connecting to local database: {host}:{port}/{db_name}")

# 3. Create the engine
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    logger.success("Sqlalchemy engine initialized")
except Exception as e:
    logger.critical(f"Failed to initialize database engine: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    logger.debug("Database session opened")
    try:
        yield db
    except Exception as e:
        logger.error(f"Error {e} in database session")
    finally:
        db.close()
        logger.debug("Database session closed")