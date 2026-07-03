#security settings
#hashing the passwod
#validating the password
#creating a token
#verifying the token


import os
from passlib.context import CryptContext
from datetime import datetime,timedelta
from jose import  JWTError, jwt
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from database import get_db


Oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/login")
load_dotenv()

password_context=CryptContext(["bcrypt"])

secret_key=os.getenv("SECRET_KEY")
algorithm=os.getenv("ALGORITHM")
expiry=int(os.getenv("EXPIRES_IN_MINS"))


def hashpassword(password:str):
    return password_context.hash(password)

def validate_password(password:str,scrambled_password:str):
    return password_context.verify(password,scrambled_password)

def create_token(data:dict):
    exp=datetime.utcnow()+ timedelta(minutes=expiry)
    data.update({"exp":exp})
    return jwt.encode(data,secret_key,algorithm=algorithm)

def verify_token(token:str):
    try:
        result=jwt.decode(token,secret_key,algorithms=[algorithm])
        username=result.get("sub")
        return username
    except JWTError:
        return None
    
def get_current_user(token:str=Depends(Oauth2_scheme),db=Depends(get_db)):
    username=verify_token(token)
    if username is None:
        raise HTTPException(status_code=401,detail="unauthorized user")
    user=db.query(User).filter(User.name == username).first()
    if user is None:
        raise HTTPException(status_code=401,detail="unauthorized user")
    return user
    
    #import user from models after creating models