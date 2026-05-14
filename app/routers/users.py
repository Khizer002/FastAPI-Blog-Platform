from .. import schemas, models, oauth2
from fastapi import status, HTTPException, APIRouter,Request,UploadFile,Depends
from ..utils import pass_hashing,process_img
from .. import dependencies as deps
from loguru import logger
from sqlalchemy import select
from ..main1 import limiter
from pathlib import Path
from ..config import settings
from uuid import uuid4
import shutil
from fastapi.concurrency import run_in_threadpool

router = APIRouter(
    prefix="/users",
    tags=["User"]
)

Upload_path=Path("static/uploads")
Upload_path.mkdir(parents=True,exist_ok=True)

MAX_SIZE=settings.MAX_FILE_UPLOAD_SIZE

def checkSize(file:deps.file):
    if file.size>MAX_SIZE:
        logger.warning(f"File size {file.size} is greater than maximum size {MAX_SIZE}")
        raise HTTPException(status_code=status.HTTP_413_CONTENT_TOO_LARGE,detail=f"File is too large. Max allowed={MAX_SIZE}")
    return file

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

@router.patch("/upload-pfp",status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("2/hour")
async def profile_photo(request:Request, current_user:oauth2.CurrentUser, db:deps.DBsession, file:UploadFile=Depends(checkSize)):
    extension=Path(file.filename).suffix
    unique_name=f"{uuid4()}{extension}"
    file_path=Upload_path / unique_name 
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    try:
        await run_in_threadpool(process_img,file_path)
        logger.success("Checking the img")
    except Exception as e:
        logger.error(f"Not a real img: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="That's not a real image")
        
    img_url=f"/static/uploads/{unique_name}"
    query=await db.execute(select(models.User).where(models.User.id==current_user.id))
    user=query.scalars().first()
    if not user:
        logger.warning("User not found, might be deleted or banned")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not Found")
    if user.profile_pic and "uploads" not in user.profile_pic:
        old_path = Path(user.profile_pic.strip("/")) 
        if old_path.exists():
            old_path.unlink() # Delete from disk
            logger.info(f"Cleanup: Old image {old_path} deleted")
    
    user.profile_pic=img_url
    await db.commit()
    await db.refresh(user) #By this the user variable be always be updated
    logger.success("Image is saved and profile_pic updated.")
    return {"message": "Profile picture updated", "url": img_url}
    