from fastapi import FastAPI
from .database import engine
from . import models
from .routers import blogs,users,auth,vote
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine)
app=FastAPI()
origins = [
    # "https://www.youtube.com",
    # "https://www.google.com"
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(blogs.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def home():
    return {"data":"Hello World"}

