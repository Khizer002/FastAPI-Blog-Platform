import jwt
from datetime import timedelta,datetime
from fastapi import HTTPException,status,Depends
from fastapi.security import OAuth2PasswordBearer
from . import models,database,schemas
from .config import settings
from sqlalchemy.orm import Session

secret_key=settings.SECRET_KEY
algorithm=settings.ALGORITHM
access_time=settings.ACCESS_TOKEN_EXPIRE_MINUTES
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def create_token(data:dict):
    to_encode=data.copy()

    expire=datetime.utcnow() + timedelta(minutes=access_time)
    to_encode.update({"exp":expire})

    token=jwt.encode(to_encode,secret_key,algorithm=algorithm)
    return token

def verify_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,secret_key,algorithms=[algorithm])
        id:str=payload.get("sub")
        if not id:
            raise credentials_exception
        return id
    except jwt.InvalidTokenError:
        raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"
                                        ,headers={"WWW-Authenticate":"Bearer"})
    token_data=verify_token(token,credentials_exception)
    user=db.query(models.User).filter(models.User.id==int(token_data)).first()
    return schemas.User_Response.model_validate(user)