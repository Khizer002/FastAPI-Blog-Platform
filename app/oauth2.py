import jwt
from datetime import timedelta, datetime
from fastapi import HTTPException, status, Depends
from . import models, schemas
from . import dependencies as deps
from .config import settings
from typing import Annotated
from loguru import logger

secret_key = settings.SECRET_KEY
algorithm = settings.ALGORITHM
access_time = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_token(data: dict):
    logger.info(f"Payload: {data.get("sub")}")
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=access_time)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    logger.success(f"Token created successfully for {data.get("sub")}")
    return token

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        id: str = payload.get("sub")
        if not id:
            logger.warning("Missing 'sub' field")
            raise credentials_exception
        return id
    except (jwt.InvalidTokenError):
        logger.info("Token expired")
        raise credentials_exception
    except(jwt.ExpiredSignatureError):
        logger.warning("Unknown person tried to access")
        raise credentials_exception
    
def get_current_user(token: deps.TokenVal, db: deps.DBsession):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token_data = verify_token(token, credentials_exception)
    logger.debug(f"Authenticating User ID: {token_data}")
    user = db.query(models.User).filter(models.User.id == int(token_data)).first()
    if not user:
        logger.warning(f"Auth Failed: User ID {token_data} not found in database.")
        raise credentials_exception
    return schemas.User_Response.model_validate(user)

CurrentUser = Annotated[schemas.User_Response, Depends(get_current_user)]