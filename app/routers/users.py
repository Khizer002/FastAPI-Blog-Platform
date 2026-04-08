from .. import schemas, models
from fastapi import status, HTTPException, APIRouter,Request
from ..utils import pass_hashing
from .. import dependencies as deps
from loguru import logger
from sqlalchemy import select
from ..main1 import limiter

router = APIRouter(
    prefix="/users",
    tags=["User"]
)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User_Response)
@limiter.limit("2/hour")
async def create_user(request:Request,user: schemas.AddUser, db: deps.DBsession):
    logger.info(f"Creating a user for {user.fullName}")
    query = await db.execute(select(models.User).where(models.User.email == user.email))
    existing_user:models.User = query.scalars().first()
    if existing_user:
        logger.warning(f"Email {user.email} is already taken")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already taken!")
    hashed_password = pass_hashing(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    logger.success(f"Created a new user with id {new_user.id}")
    return new_user

@router.get("/{id}", response_model=schemas.User_Response)
@limiter.limit("40/minute")
async def get_users(request:Request,id: deps.BlogID, db: deps.DBsession):
    logger.info(f"Retreving info of user with id:{id}")
    query = await db.execute(select(models.User).where(models.User.id == id))
    user:models.User = query.scalars().first()
    if not user:
        logger.warning(f"There was no user with id:{id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    logger.info(f"User found: {user.fullName} and id: {user.id}")
    return user
