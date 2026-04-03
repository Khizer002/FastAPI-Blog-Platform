from fastapi import FastAPI,Request
from .database import engine
from .routers import blogs,users,auth,vote
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk
from .logging_config import setup_logging
from .config import settings
from loguru import logger
import time
from contextlib import asynccontextmanager


setup_logging()
if settings.SENTRY_DSN:
    sentry_sdk.init(dsn=settings.SENTRY_DSN, environment=settings.ENV, traces_sample_rate=1.0)
# models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info("Starting up: Initializing database connection pool")
    yield
    logger.info("Shutting down: Database connection pool")
    await engine.dispose

app=FastAPI(title="Blog-Platform", lifespan=lifespan)

@app.middleware("http")
async def log_requests(request:Request,call_next):
    logger.info(f"Incoming: {request.method} {request.url.path}")
    start_time=time.perf_counter()
    response=await call_next(request)
    end_time=time.perf_counter()-start_time

    logger.success(f"Completed: {request.method} {request.url.path} | Status: {response.status_code} | {end_time:.4f}s")
    return response

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
    logger.info("Hey this is starting route: ")
    return {"data":"Hello World"}
