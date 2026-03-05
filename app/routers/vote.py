from fastapi import APIRouter,status,HTTPException,Depends
from .. import schemas,models,oauth2,database
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/vote",
    tags=["Voting"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def like_blog(info:schemas.Vote,current_user:schemas.User_Response=Depends(oauth2.get_current_user),db:Session=Depends(database.get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==info.post_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There is not blog with this id: {info.post_id}")
    blog_query=db.query(models.Vote).filter(models.Vote.post_id==info.post_id,models.Vote.user_id==current_user.id)
    found_vote=blog_query.first()
    if info.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Already voted")
        new_vote=models.Vote(post_id=info.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")
        blog_query.delete(found_vote,synchronize_session=False)
        db.commit()
        return {"message":"Vote deleted successfully"}