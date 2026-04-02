import logging
import sys
from loguru import logger
from .config import settings

class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

def setup_logging():
    logger.remove()

    if settings.ENV == "prod":
        logger.add(sys.stdout, serialize=True, level="INFO")
    else:
        logger.add(
            sys.stdout, 
            level="DEBUG",
            colorize=True, 
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )

    logger.add(
        "logs/app.log",
        rotation="500 MB",
        retention="10 days",
        compression="zip", 
        level="SUCCESS",    
        enqueue=True,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )