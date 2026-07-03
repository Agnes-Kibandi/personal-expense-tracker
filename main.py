from fastapi import FastAPI
from database import Base,engine

app=FastAPI()

Base.metadata.createall(bind=engine)