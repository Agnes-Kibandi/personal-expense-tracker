from fastapi import FastAPI
from database import Base,engine
from routers import auth, expenses
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
app.include_router(auth.router)
app.include_router((expenses.router))

origins=["http://localhost"
         "http://myapp.vercel.app"]

Base.metadata.createall(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origin=origins,
    allow_headers="[*]",
    allow__methods="[*]",
    allow_credentials=True
)

@app.middleware