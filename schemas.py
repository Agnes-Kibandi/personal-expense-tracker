from pydantic import BaseModel
from typing import Optional
from datetime import date

class Token(BaseModel):
    access_token:str
    token_type:str

class UserIn(BaseModel):
    name: str
    email:str
    password:str


class UserOut(BaseModel):
    model_config={'from_attributes':True}
    name:str
    email:str

class ExpenseIn(BaseModel):
    title:str
    amount:float
    category:str
    date:date

class ExpenseOut(BaseModel):
    model_config={'from_attributes':True}
    id:int
    title:str
    amount:float
    category:str
    date:date

    


class ExpenseUpdate(BaseModel):
    title:Optional[str]=None
    amount:Optional [float] = None
    category:Optional [str] = None
    date:Optional [date] = None


class UserUpdate(BaseModel):
    name:Optional[str]=None
    email:Optional [str]=None
    password:Optional [str] = None
   