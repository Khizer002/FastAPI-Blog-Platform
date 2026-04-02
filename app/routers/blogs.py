from .. import schemas, models, oauth2
from fastapi import status, HTTPException, APIRouter, Response
from typing import List
from sqlalchemy import func
from .. import dependencies as deps
from loguru import logger

router = APIRouter(
    prefix="/blogs",
    tags=["Blog"]
)

@router.get("/", response_model=List[schemas.BlogOut])
def blogs(db: deps.DBsession, current_user: oauth2.CurrentUser, limit: deps.Limit = 10, skip: deps.Skip = 0, search: deps.Search = None):
    logger.info(f"User {current_user.id} fetching blogs | Limit: {limit} | Skip: {skip}")
    # cursor=conn.cursor(dictionary=True)
    # cursor.execute("select * from blogs;")
    # og_rows=cursor.fetchall()
    logger.debug(f"Username {current_user.email}")
    query = db.query(models.Blog, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Blog.id == models.Vote.post_id, isouter=True).group_by(models.Blog.id)
    if search:
        logger.debug(f"Searched for: {search}")
        query=query.filter(models.Blog.title.contains(search))
    query_res = query.limit(limit).offset(skip).all()
    logger.info(f"Retrived all {len(query_res)} blogs")
    return query_res

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Response_blogs)
def createBlog(payload: schemas.Payload, db: deps.DBsession, current_user: oauth2.CurrentUser):
    logger.info(f"User id: {current_user.id}")
    # cursor=conn.cursor(dictionary=True)
    # cursor.execute("insert into blogs (title,content) values(%s,%s) ",(payload.title,payload.content,))
    # conn.commit()
    # blog_id=cursor.lastrowid
    # cursor.execute("select * from blogs where id=%s",(blog_id,))
    # new_blog=cursor.fetchone()
    logger.debug(f"Payload: {payload.model_dump()}")
    new_blog = models.Blog(owner_id=current_user.id, **payload.model_dump())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    logger.success(f"Blog {new_blog.id} added by user: {current_user.fullName}")
    return new_blog

@router.get("/{id}", response_model=schemas.BlogOut)
def get_blog(id: deps.BlogID, db: deps.DBsession, current_user: oauth2.CurrentUser):
    logger.info(f"User id: {current_user.id}")
    # cursor=conn.cursor(dictionary=True)
    # cursor.execute("select * from blogs where id=%s",(str(id),))
    # blog=cursor.fetchone()
    logger.debug(f"ID to search was: {id}")
    blog = db.query(models.Blog, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Blog.id == models.Vote.post_id, isouter=True).group_by(models.Blog.id).filter(models.Blog.id == id).first()
    if not blog:
        logger.warning(f"We cant find any blog with this id: {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    logger.info(f"Data Retrevied: Blog was made by: {blog[0].owner.fullName}")
    return blog

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: deps.BlogID, db: deps.DBsession, current_user: oauth2.CurrentUser):
    logger.info(f"User id: {current_user.id}")
    # cursor=conn.cursor(dictionary=True)
    # cursor.execute("delete from blogs where id=%s",(id,))
    # conn.commit()
    # deleted_id=cursor.rowcount
    deleted_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if deleted_blog == None:
        logger.warning(f"We cant find any blog with this id: {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"there is nothing with this id of {id}")
    if deleted_blog.owner_id != current_user.id:
        logger.warning(f"Ids dont match he is not the owner: {deleted_blog.owner_id} and current user id: {current_user.id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="U are not allowed to do this")
    db.delete(deleted_blog)
    db.commit()
    logger.success(f"Blog {id} is deleted")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Response_blogs)
def update_blog(id: deps.BlogID, blog: schemas.update_blog_data, db: deps.DBsession, current_user: oauth2.CurrentUser):
    logger.info(f"User id: {current_user.id}")
    # cursor=conn.cursor(dictionary=True)
    # cursor.execute("update blogs set title=%s,content=%s,published=%s where id=%s",(blog.title,blog.content,blog.published,str(id),))
    # conn.commit()
    # if cursor.rowcount==0:
    #     raise HTTPException(status_code=404,detail=f"There is nothing to update with this {id}")
    # cursor.execute("select * from blogs where id=%s",(str(id),))
    # updated_row=cursor.fetchone()
    updated_row_query = db.query(models.Blog).filter(models.Blog.id == id)
    updated_row = updated_row_query.first()
    if updated_row == None:
        logger.warning(f"We cant find any blog with this id: {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is nothing to update with this id {id}")
    if updated_row.owner_id != current_user.id:
        logger.warning(f"Ids dont match he is not the owner: {updated_row.owner_id} and current user id: {current_user.id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="U are not allowed to do this")
    updated_row_query.update(blog.model_dump(), synchronize_session=False)
    db.commit()
    logger.success(f"Blog {id} is updated")
    return updated_row_query.first()

@router.patch("/{id}", response_model=schemas.Response_blogs)
def update_blogViaPatch(id: deps.BlogID, blog: schemas.updateBlog, db: deps.DBsession, current_user: oauth2.CurrentUser):
    logger.info(f"User id: {current_user.id}")
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
    updated_rowViaPatch = db.query(models.Blog).filter(models.Blog.id == id)
    updated_row = updated_rowViaPatch.first()
    if updated_row == None:
        logger.warning(f"We cant find any blog with this id: {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is nothing to update with this id {id}")
    if updated_row.owner_id != current_user.id:
        logger.warning(f"Ids dont match he is not the owner: {updated_row.owner_id} and current user id: {current_user.id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="U are not allowed to do this")
    updated_rowViaPatch.update(blog.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    logger.success(f"Blog {id} is updated")
    return updated_rowViaPatch.first()