from .. import schemas, models, oauth2
from fastapi import status, HTTPException, APIRouter, Response
from typing import List
from sqlalchemy import func
from .. import dependencies as deps
from loguru import logger
from sqlalchemy import select,delete,update
from sqlalchemy.orm import selectinload

router = APIRouter(
    prefix="/blogs",
    tags=["Blog"]
)

@router.get("/", response_model=List[schemas.BlogOut])
async def blogs(db: deps.DBsession, current_user: oauth2.CurrentUser, limit: deps.Limit = 10, skip: deps.Skip = 0, search: deps.Search = None):
    logger.info(f"User {current_user.id} fetching blogs | Limit: {limit} | Skip: {skip}")
    # cursor=conn.cursor(dictionary=True)
    # cursor.execute("select * from blogs;")
    # og_rows=cursor.fetchall()
    logger.debug(f"Username {current_user.email}")
    stmt = (
        select(models.Blog, func.count(models.Vote.post_id).label("likes"))
        .join(models.Vote, models.Blog.id == models.Vote.post_id, isouter=True)
        .group_by(models.Blog.id)
        .options(selectinload(models.Blog.owner)) 
    )
    if search:
        logger.debug(f"Filtering by search: {search}")
        stmt = stmt.where(models.Blog.title.contains(search))
    stmt = stmt.limit(limit).offset(skip)
    result = await db.execute(stmt)
    blogs_with_likes:models.Blog = result.all()
    logger.info(f"Retrived all {len(blogs_with_likes)} blogs")
    return blogs_with_likes

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Response_blogs)
async def createBlog(payload: schemas.Payload, db: deps.DBsession, current_user: oauth2.CurrentUser):
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
    await db.commit()
    await db.refresh(new_blog,attribute_names=["owner","created_At"])
    logger.success(f"Blog {new_blog.id} added by user: {current_user.fullName}")
    return new_blog

@router.get("/{id}", response_model=schemas.BlogOut)
async def get_blog(id: deps.BlogID, db: deps.DBsession, current_user: oauth2.CurrentUser):
    logger.info(f"User id: {current_user.id}")
    # cursor=conn.cursor(dictionary=True)
    # cursor.execute("select * from blogs where id=%s",(str(id),))
    # blog=cursor.fetchone()
    logger.debug(f"ID to search was: {id}")
    stmt= await db.execute(select(models.Blog, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Blog.id == models.Vote.post_id, isouter=True).group_by(models.Blog.id).options(selectinload(models.Blog.owner)).where(models.Blog.id == id))
    blog:models.Blog=stmt.first()
    if not blog:
        logger.warning(f"We cant find any blog with this id: {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    logger.info(f"Data Retrevied: Blog was made by: {blog[0].owner.fullName}")
    return blog

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id: deps.BlogID, db: deps.DBsession, current_user: oauth2.CurrentUser):
    logger.info(f"User id: {current_user.id}")
    # cursor=conn.cursor(dictionary=True)
    # cursor.execute("delete from blogs where id=%s",(id,))
    # conn.commit()
    # deleted_id=cursor.rowcount
    stmt = await db.execute(select(models.Blog).where(models.Blog.id == id))
    deleted_blog:models.Blog =stmt.scalars().first()
    if deleted_blog == None:
        logger.warning(f"We cant find any blog with this id: {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"there is nothing with this id of {id}")
    if deleted_blog.owner_id != current_user.id:
        logger.warning(f"Ids dont match he is not the owner: {deleted_blog.owner_id} and current user id: {current_user.id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="U are not allowed to do this")
    await db.delete(deleted_blog)
    await db.commit()
    logger.success(f"Blog {id} is deleted")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Response_blogs)
async def update_blog(id: deps.BlogID, blog: schemas.update_blog_data, db: deps.DBsession, current_user: oauth2.CurrentUser):
    logger.info(f"User id: {current_user.id}")
    # cursor=conn.cursor(dictionary=True)
    # cursor.execute("update blogs set title=%s,content=%s,published=%s where id=%s",(blog.title,blog.content,blog.published,str(id),))
    # conn.commit()
    # if cursor.rowcount==0:
    #     raise HTTPException(status_code=404,detail=f"There is nothing to update with this {id}")
    # cursor.execute("select * from blogs where id=%s",(str(id),))
    # updated_row=cursor.fetchone()
    updated_row_query = await db.execute(select(models.Blog).where(models.Blog.id == id))
    updated_row:models.Blog = updated_row_query.scalars().first()
    if updated_row == None:
        logger.warning(f"We cant find any blog with this id: {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is nothing to update with this id {id}")
    if updated_row.owner_id != current_user.id:
        logger.warning(f"Ids dont match he is not the owner: {updated_row.owner_id} and current user id: {current_user.id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="U are not allowed to do this")
    update_stmt = (
        update(models.Blog)
        .where(models.Blog.id == id)
        .values(**blog.model_dump()) 
        .execution_options(synchronize_session="fetch") 
    )
    await db.execute(update_stmt)
    await db.commit()
    await db.refresh(updated_row,attribute_names=["owner"])
    logger.success(f"Blog {id} is updated")
    return updated_row

@router.patch("/{id}", response_model=schemas.Response_blogs)
async def update_blogViaPatch(id: deps.BlogID, blog: schemas.updateBlog, db: deps.DBsession, current_user: oauth2.CurrentUser):
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
    updated_rowViaPatch = await db.execute(select(models.Blog).where(models.Blog.id == id))
    updated_row:models.Blog = updated_rowViaPatch.scalars().first()
    if updated_row == None:
        logger.warning(f"We cant find any blog with this id: {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is nothing to update with this id {id}")
    if updated_row.owner_id != current_user.id:
        logger.warning(f"Ids dont match he is not the owner: {updated_row.owner_id} and current user id: {current_user.id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="U are not allowed to do this")
    update_stmt = (
        update(models.Blog)
        .where(models.Blog.id == id)
        .values(**blog.model_dump(exclude_unset=True)) 
        .execution_options(synchronize_session="fetch") 
    )
    await db.execute(update_stmt)
    await db.commit()
    await db.refresh(updated_row,attribute_names=["owner"])
    logger.success(f"Blog {id} is updated")
    return updated_row