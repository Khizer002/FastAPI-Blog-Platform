from fastapi import Query, Path, Depends
from pydantic import Field
from typing import Optional, Annotated
from .database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

DBsession = Annotated[Session, Depends(get_db)]
RequestForm = Annotated[OAuth2PasswordRequestForm, Depends()]
TokenVal = Annotated[str, Depends(oauth2_scheme)]

Title = Annotated[str, Field(description="Write title of your fav hobby", min_length=3, max_length=15)]
Content = Annotated[str, Field(description="Describe your hobby", min_length=10, max_length=100)]
Published = Annotated[Optional[bool], Query(description="Whether the blog is live or not")]
BlogID = Annotated[int, Path(title="ID for the blogs", ge=1)]
Limit = Annotated[int, Query(description="Pagination limit", ge=1, le=100)]
Skip = Annotated[int, Query(description="Skip some", ge=0, le=100)]
Search = Annotated[Optional[str], Query(description="Search by title", min_length=3, max_length=15)]
DirID = Annotated[int, Field(description="whether blog is liked or not", ge=0, le=1)]
FullName = Annotated[str, Field(pattern=r"^[a-zA-Z]+\s+[a-zA-Z]+$", description="Firstname and Lastname")]
PASSWORD = Annotated[str, Field(min_length=8, description="Set password with at least 8 characters")]