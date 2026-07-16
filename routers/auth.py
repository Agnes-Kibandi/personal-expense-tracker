from fastapi import APIRouter
from schemas import UserIn,UserOut,Token
from database import get_db
from fastapi import Depends, HTTPException
from auth import hashpassword,create_token,validate_password,get_current_user
from models  import User as Usermodel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#signup
#login
#currently logged in user

router= APIRouter(prefix="/auth", tags=["auth"])



@router.post("/register",response_model=UserOut)
def signup(user:UserIn,db=Depends(get_db)):
    hashed_password1= hashpassword(user.password)
    db_user=Usermodel(
        name=user.name,
        email=user.email,
        hashed_password= hashed_password1
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post("/login", response_model= Token)
def login(form_data:OAuth2PasswordRequestForm=Depends(), db=Depends(get_db)):
    user = db.query(Usermodel).filter(Usermodel.name==form_data.username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="user not found")
    username= user.name

    if not validate_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=401,detail="user not found")
    token = create_token({"sub":username})
    return {"access_token": token, "token_type": "bearer"}

    
@router.get("/me", response_model= UserOut)
def curently_logged_in(user=Depends(get_current_user) ):
    return user  
    