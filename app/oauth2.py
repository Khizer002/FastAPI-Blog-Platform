import jwt
from datetime import timedelta, datetime
from fastapi import HTTPException, status, Depends
from . import models, schemas
from . import dependencies as deps
from .config import settings
from typing import Annotated
from loguru import logger
from sqlalchemy import select

secret_key = settings.SECRET_KEY
algorithm = settings.ALGORITHM
access_time = settings.ACCESS_TOKEN_EXPIRE_MINUTES
refresh_secret_key=settings.REFRESH_SECRET_KEY
refresh_time=settings.REFRESH_TOKEN_EXPIRE_DAYS

def create_token(data: dict):
    logger.info(f"Payload: {data.get("sub")}")
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=access_time)
    to_encode.update({"exp": expire,"type":"access"})
    token = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    logger.success(f"Token created successfully for {data.get("sub")}")
    return token

def create_refresh_token(data: dict):
    logger.info(f"Payload: {data.get("sub")}")
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=refresh_time)
    to_encode.update({"exp": expire,"type":"refresh"})
    token = jwt.encode(to_encode, refresh_secret_key, algorithm=algorithm)
    logger.success(f"Token created successfully for {data.get("sub")}")
    return token

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        id: str = payload.get("sub")
        token_type=payload.get("type")
        if not id:
            logger.warning("Missing 'sub' field")
            raise credentials_exception
        if token_type!="access":
            logger.error(f"Wrong token type used : {token_type}")
            raise credentials_exception
        return id
    except (jwt.InvalidTokenError):
        logger.info("Token expired")
        raise credentials_exception
    except(jwt.ExpiredSignatureError):
        logger.warning("Unknown person tried to access")
        raise credentials_exception

def verify_refresh_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, refresh_secret_key, algorithms=[algorithm])
        
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type") 

        if not user_id:
            logger.warning("Token payload missing 'sub'")
            raise credentials_exception
        
        if token_type != "refresh":
            logger.error(f"Wrong token type used: {token_type}")
            raise credentials_exception
            
        return user_id

    except jwt.ExpiredSignatureError:
        logger.warning("Refresh token has expired")
        raise credentials_exception
    except jwt.JWTError: 
        logger.info("Invalid token signature or format")
        raise credentials_exception
    
async def get_current_user(token: deps.TokenVal, db: deps.DBsession):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token_data = verify_token(token, credentials_exception)
    logger.debug(f"Authenticating User ID: {token_data}")
    query = await db.execute(select(models.User).where(models.User.id == int(token_data)))
    user:models.User=query.scalars().first()
    if not user:
        logger.warning(f"Auth Failed: User ID {token_data} not found in database.")
        raise credentials_exception
    return schemas.User_Response.model_validate(user)

CurrentUser = Annotated[schemas.User_Response, Depends(get_current_user)]