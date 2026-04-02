from fastapi import APIRouter, status, HTTPException
from .. import models, oauth2, schemas
from .. import dependencies as deps
from loguru import logger

router = APIRouter(
    prefix="/vote",
    tags=["Voting"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def like_blog(info: schemas.AddVote, current_user: oauth2.CurrentUser, db: deps.DBsession):
    logger.info(f"User id: {current_user.id}")
    blog = db.query(models.Blog).filter(models.Blog.id == info.post_id).first()
    if not blog:
        logger.warning(f"There was no blog with this id:{info.post_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is not blog with this id: {info.post_id}")
    blog_query = db.query(models.Vote).filter(models.Vote.post_id == info.post_id, models.Vote.user_id == current_user.id)
    found_vote = blog_query.first()
    if info.dir == 1:
        if found_vote:
            logger.warning(f"User {current_user.id} tried to double-vote on Blog {info.post_id}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Already voted")
        new_vote = models.Vote(post_id = info.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        logger.success(f"Vote added to blog {info.post_id}")
        return {"message": "Vote added successfully"}
    else:
        if not found_vote:
            logger.warning(f"User {current_user.id} tried to delete a non-existent vote on Blog {info.post_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        blog_query.delete(synchronize_session = False)
        db.commit()
        logger.success(f"Vote deleted for blog {info.post_id}")
        return {"message": "Vote deleted successfully"}