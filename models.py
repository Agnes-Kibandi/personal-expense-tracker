from sqlalchemy import Column,Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Expense(Base):
    __tablename__="expenses"
    id=Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    owner=relationship("User", back_populates="expenses")
    title=Column(String)
    amount=Column(Float)
    category=Column(String)
    date=Column(Date)


class User(Base):
    __tablename__= "users"
    id=Column(Integer,primary_key=True)
    expenses=relationship("Expense", back_populates="owner")
    name= Column(String)
    email= Column(String)
    hashed_password=Column(String)
    
