from .. import schemas,models,oauth2
from sqlalchemy.orm import Session
from fastapi import status,Depends,HTTPException,APIRouter,Response
from ..database import get_db
from typing import List,Optional
from sqlalchemy import func

router=APIRouter(
    prefix="/blogs",
    tags=["Blog"]
)

@router.get("/",response_model=List[schemas.BlogOut])
def blogs(db:Session=Depends(get_db),current_user:schemas.User_Response=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    # cursor=conn.cursor(dictionary=True)
    # cursor.execute("select * from blogs;")
    # og_rows=cursor.fetchall()
    query=db.query(models.Blog,func.count(models.Vote.post_id).label("likes")).join(models.Vote,models.Blog.id==models.Vote.post_id,isouter=True).group_by(models.Blog.id).filter(models.Blog.title.contains(search)).limit(limit).offset(skip)
    query_res=query.all()
    return query_res

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Response_blogs)
def createBlog(payload:schemas.insert_blog,db:Session=Depends(get_db),current_user:schemas.User_Response=Depends(oauth2.get_current_user)):
    # cursor=conn.cursor(dictionary=True)
    # cursor.execute("insert into blogs (title,content) values(%s,%s) ",(payload.title,payload.content,))
    # conn.commit()
    # blog_id=cursor.lastrowid
    # cursor.execute("select * from blogs where id=%s",(blog_id,))
    # new_blog=cursor.fetchone()
    new_blog=models.Blog(owner_id=current_user.id,**payload.dict())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/{id}",response_model=schemas.BlogOut)
def get_blog(id:int,db:Session=Depends(get_db),current_user:schemas.User_Response=Depends(oauth2.get_current_user)):
    # cursor=conn.cursor(dictionary=True)
    # cursor.execute("select * from blogs where id=%s",(str(id),))
    # blog=cursor.fetchone()
    blog=db.query(models.Blog,func.count(models.Vote.post_id).label("likes")).join(models.Vote,models.Blog.id==models.Vote.post_id,isouter=True).group_by(models.Blog.id).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not Found")
    return blog

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id:int,db:Session=Depends(get_db),current_user:schemas.User_Response=Depends(oauth2.get_current_user)):
    # cursor=conn.cursor(dictionary=True)
    # cursor.execute("delete from blogs where id=%s",(id,))
    # conn.commit()
    # deleted_id=cursor.rowcount
    deleted_blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if deleted_blog==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"there is nothing with this id of {id}")
    if deleted_blog.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="U are not allowed to do this")
    db.delete(deleted_blog)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Response_blogs)
def update_blog(id:int,blog:schemas.Blog,db:Session=Depends(get_db),current_user:schemas.User_Response=Depends(oauth2.get_current_user)):
    # cursor=conn.cursor(dictionary=True)
    # cursor.execute("update blogs set title=%s,content=%s,published=%s where id=%s",(blog.title,blog.content,blog.published,str(id),))
    # conn.commit()
    # if cursor.rowcount==0:
    #     raise HTTPException(status_code=404,detail=f"There is nothing to update with this {id}")
    # cursor.execute("select * from blogs where id=%s",(str(id),))
    # updated_row=cursor.fetchone()
    updated_row_query=db.query(models.Blog).filter(models.Blog.id==id)
    updated_row=updated_row_query.first()
    if updated_row==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There is nothing to update with this id {id}")
    if updated_row.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="U are not allowed to do this")
    updated_row_query.update(blog.dict(),synchronize_session=False)
    db.commit()
    return updated_row_query.first()

@router.patch("/{id}",response_model=schemas.Response_blogs)
def update_blogViaPatch(id:int,blog:schemas.updateBlog,db:Session=Depends(get_db),current_user:schemas.User_Response=Depends(oauth2.get_current_user)):
    # cursor=conn.cursor(dictionary=True)
    # updated_data=blog.dict(exclude_unset=True)
    # if updated_data==None:
    #     raise HTTPException(status_code=400,detail=f"No data provided to update")
    # fields=[]
    # values=[]
    # for key,value in updated_data.items():
    #     fields.append(f"{key}=%s")
    #     values.append(value)
    #     values.append(id)
    # query=f"update blogs set {(",").join(fields)} where id=%s"
    # cursor.execute(query,tuple(values))
    # conn.commit()
    # if cursor.rowcount==0:
    #     raise HTTPException(status_code=404,detail=f"Nothing to update with this id {id}")
    # cursor.execute("select * from blogs where id=%s",(id,))
    # updated_rowViaPatch=cursor.fetchone()
    updated_rowViaPatch=db.query(models.Blog).filter(models.Blog.id==id)
    updated_row=updated_rowViaPatch.first()
    if updated_row==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"There is nothing to update with this id {id}")
    if updated_row.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="U are not allowed to do this")
    updated_rowViaPatch.update(blog.dict(exclude_unset=True),synchronize_session=False)
    db.commit()
    return updated_rowViaPatch.first()