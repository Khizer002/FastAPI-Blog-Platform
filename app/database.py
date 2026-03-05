from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import mysql.connector
from .config import settings

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base= declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

# try:
#     conn=mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="khizer",
#         database="fastapi",
#         port="3306"
#     )
#     print("Database is connected: ")
# except Exception as e:
#     print("Error: ",e)
#     time.sleep(2)