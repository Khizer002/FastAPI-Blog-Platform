from .. import schemas, utils, models, oauth2
from fastapi import HTTPException, status, APIRouter
from .. import dependencies as deps
from loguru import logger

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login_user(user_credentials: deps.RequestForm, db: deps.DBsession):
    logger.debug(f"User_Credentials: {user_credentials.username}")
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username
    ).first()

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

    jwt_token = oauth2.create_token({"sub": str(user.id)})
    logger.success(f"Successfully authenticated User ID: {user.id} ({user_credentials.username})")
    return {
        "access_token": jwt_token,
        "token_type": "bearer"
    }