from fastapi import FastAPI,Request
from database import Base,engine
from routers import auth, expenses
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse



@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(bind=engine)
    print("One day at a time.You can do it")
    yield



app=FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router((expenses.router))

origins=["http://localhost",
         "http://myapp.vercel.app"]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_headers=["*"],
    allow__methods=["*"],
    allow_credentials=True
)



@app.middleware("http")
async def add_header(request:Request,call_next):
    response=await call_next(request)
    response.headers["X-Kui_Kibandy"]="fabulous"
    return response

class UserNotFound(Exception):
    def __init__(self, user_id:int):
        self.user_id=user_id

@app.exception_handler(UserNotFound)
async def user_not_found_handler(request:Request,exc:UserNotFound):
    return JSONResponse(
        status_code=404,
        content={
            "message":f"there's no one by this {exc.user_id}"
        }
    )
       
        