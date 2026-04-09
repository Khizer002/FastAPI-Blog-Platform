from .. import schemas, utils, models, oauth2
from fastapi import HTTPException, status, APIRouter,Request
from .. import dependencies as deps
from loguru import logger
from sqlalchemy import select,delete
from ..main1 import limiter

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
@limiter.limit("5/minute")
async def login_user(request:Request,user_credentials: deps.RequestForm, db: deps.DBsession):
    logger.debug(f"User_Credentials: {user_credentials.username}")
    query = await db.execute(select(models.User).filter(
        models.User.email == user_credentials.username
    ))
    user = query.scalars().first()

    if not user:
        logger.warning(f"User {user_credentials.username} has enetered wrong credentials")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )

    if not utils.pass_verify(user_credentials.password, user.password):
        logger.warning(f"User {user_credentials.username} has enetered wrong credentials")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )

    jwt_access_token = oauth2.create_token({"sub": str(user.id)})
    jwt_refresh_token = oauth2.create_refresh_token({"sub":str(user.id)})
    new_db_token=models.RefreshToken(user_id=user.id,token=jwt_refresh_token)
    db.add(new_db_token)
    await db.commit()
    logger.success(f"Successfully authenticated User ID: {user.id} ({user_credentials.username})")
    return {
        "access_token": jwt_access_token,
        "refresh_token":jwt_refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=schemas.Token)
@limiter.limit("5/minute")
async def refresh_token(request:Request,payload: schemas.Refresh_token_schema, db: deps.DBsession):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_query=await db.execute(select(models.RefreshToken).where(models.RefreshToken.token==payload.refresh_token))
    token=token_query.scalars().first()
    if not token:
        logger.error(f"Invalid refresh token {payload.refresh_token}")
        raise credentials_exception
    
    if token.is_used==True:
        await db.execute(
            delete(models.RefreshToken).where(models.RefreshToken.user_id == token.user_id)
        )
        await db.commit()
        logger.warning(f"REUSE DETECTED for User {token.user_id}. All sessions revoked.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Security breach detected. Please log in again.")
    
    user_id = oauth2.verify_refresh_token(payload.refresh_token, credentials_exception)
    query = await db.execute(select(models.User).where(models.User.id == user_id))
    user = query.scalars().first()
    
    if not user:
        logger.warning(f"Refresh attempted for non-existent user ID: {user_id}")
        raise credentials_exception
    
    token.is_used=True
    
    new_access_token = oauth2.create_token({"sub": str(user.id)})
    new_refresh_token = oauth2.create_refresh_token({"sub": str(user.id)})
    new_db_token=models.RefreshToken(user_id=user.id,token=new_refresh_token)
    db.add(new_db_token)
    await db.commit()
    logger.success(f"Token rotated successfully for user: {user.email}")
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }