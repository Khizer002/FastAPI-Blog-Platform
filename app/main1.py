from fastapi import FastAPI,Request
from .database import engine
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk
from .logging_config import setup_logging
from .config import settings
from loguru import logger
import time
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware


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

limiter=Limiter(key_func=get_remote_address,default_limits=["50/minute"])
app=FastAPI(title="Blog-Platform", lifespan=lifespan)
app.state.limiter=limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)

@app.middleware("http")
async def log_requests(request:Request,call_next):
    logger.info(f"Incoming: {request.method} {request.url.path}")
    start_time=time.perf_counter()
    response=await call_next(request)
    end_time=time.perf_counter()-start_time

    logger.success(f"Completed: {request.method} {request.url.path} | Status: {response.status_code} | {end_time:.4f}s")
    return response

app.add_middleware(SlowAPIMiddleware)

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .routers import blogs,users,auth,vote
app.include_router(users.router)
app.include_router(blogs.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def home():
    logger.info("Hey this is starting route: ")
    return {"data":"Hello World"}
