from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["argon2"],deprecated="auto")

def pass_hashing(password:str):
    return pwd_context.hash(password)

def pass_verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)