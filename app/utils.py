from passlib.context import CryptContext
from PIL import Image
import dependencies as deps
from loguru import logger

pwd_context=CryptContext(schemes=["argon2"],deprecated="auto")

def pass_hashing(password:str):
    return pwd_context.hash(password)

def pass_verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def process_img(file_path:deps.file_path):
    try:
        with Image.open(file_path) as img:
            if img.mode in ("RGBA","P"):
                img=img.convert("RGB")

            img.thumbnail((300,300))
            ext = file_path.suffix.lower()
            save_format = "PNG" if ext == ".png" else "JPEG"
            
            img.save(file_path, format=save_format, quality=85, optimize=True)
        logger.success(f"File {file_path} is valid to process.")
    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        logger.error(f"File is not valid so it is removed: {e}")
        raise ValueError("Invalid Image")
