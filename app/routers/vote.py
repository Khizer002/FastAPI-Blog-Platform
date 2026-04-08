from fastapi import APIRouter, status, HTTPException,Request
from .. import models, oauth2, schemas
from .. import dependencies as deps
from loguru import logger
from sqlalchemy import select,delete
from ..main1 import limiter

router = APIRouter(
    prefix="/vote",
    tags=["Voting"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("40/minute")
async def like_blog(request:Request,info: schemas.AddVote, current_user: oauth2.CurrentUser, db: deps.DBsession):
    logger.info(f"User id: {current_user.id}")
    query_blog = await db.execute(select(models.Blog).where(models.Blog.id == info.post_id))
    blog:models.Blog=query_blog.scalars().first()
    if not blog:
        logger.warning(f"There was no blog with this id:{info.post_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is not blog with this id: {info.post_id}")
    blog_query = await db.execute(select(models.Vote).where(models.Vote.post_id == info.post_id, models.Vote.user_id == current_user.id))
    found_vote:models.Vote = blog_query.scalars().first()
    if info.dir == 1:
        if found_vote:
            logger.warning(f"User {current_user.id} tried to double-vote on Blog {info.post_id}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Already voted")
        new_vote = models.Vote(post_id = info.post_id, user_id = current_user.id)
        db.add(new_vote)
        await db.commit()
        logger.success(f"Vote added to blog {info.post_id}")
        return {"message": "Vote added successfully"}
    else:
        if not found_vote:
            logger.warning(f"User {current_user.id} tried to delete a non-existent vote on Blog {info.post_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        delete_stmt = delete(models.Vote).where(
            models.Vote.post_id == info.post_id, 
            models.Vote.user_id == current_user.id
        )
        await db.execute(delete_stmt)
        await db.commit()
        logger.success(f"Vote deleted for blog {info.post_id}")
        return {"message": "Vote deleted successfully"}