from fastapi import FastAPI
from random import randrange
import sqlalchemy
from sqlalchemy.exc import IntegrityError
from fastapi import Depends
from . import models
from .database import engine
from .routers import post, user,Auth


models.Base.metadata.create_all(bind=engine) #this will create the tables in the database if they don't exist already

app=FastAPI()
app.include_router(user.router)
app.include_router(post.router)
app.include_router(Auth.router)




@app.get("/")
async def root():
    return {"message": "Hello World"}

 




