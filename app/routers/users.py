from .. import schemas, models
from fastapi import status, HTTPException, APIRouter
from ..utils import pass_hashing
from .. import dependencies as deps

router = APIRouter(
    prefix="/users",
    tags=["User"]
)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User_Response)
def create_user(user: schemas.AddUser, db: deps.DBsession):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already taken!")
    hashed_password = pass_hashing(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.User_Response)
def get_users(id: deps.BlogID, db: deps.DBsession):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user
