from .. import schemas,utils,models,oauth2
from fastapi import HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi.security import OAuth2PasswordRequestForm

router=APIRouter(
    tags=["Authentication"]
)
@router.post("/login", response_model=schemas.Token)
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(),
               db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )

    if not utils.pass_verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )

    jwt_token = oauth2.create_token({"sub": str(user.id)})

    return {
        "access_token": jwt_token,
        "token_type": "bearer"
    }
