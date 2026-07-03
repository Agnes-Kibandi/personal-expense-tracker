#location
#connection
#conversation
#foundation

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

database_location= os.getenv("DATABASEURL")

engine=create_engine(database_location,connect_args="check_same_thread":False)
#connect_ags agument is specific to sqlite

SessionLocal=sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base= declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()