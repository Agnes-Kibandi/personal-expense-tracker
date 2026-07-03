from fastapi import FastAPI
from database import Base,engine
from routers import auth, expenses

app=FastAPI()

Base.metadata.createall(bind=engine)