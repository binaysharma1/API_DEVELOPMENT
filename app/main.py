from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
# from pydantic import BaseModel
from typing import Optional,List
from random import randrange
import psycopg2

from psycopg2.extras import RealDictCursor
import time 
import sqlalchemy
from  sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import Depends

from . import models,schemas,utils
from .database import engine,get_db
from .routers import post, user


models.Base.metadata.create_all(bind=engine) #this will create the tables in the database if they don't exist already

app=FastAPI()
app.include_router(user.router)
app.include_router(post.router)


    
while True:  
    try:
        conn=psycopg2.connect(host='localhost',database='db_1',user='postgres',password='funk',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection was successful")
        break;
    except Exception as error:
        print("Database connection failed")
        print("Error:",error)
        time.sleep(2)


# my_posts = [{"id": 1, "title": "Post 1", "content": "Content of post 1", "published": True, "rating": 5},
#             {"id": 2, "title": "Post 2", "content": "Content of post 2", "published": False, "rating": 3}]
@app.get("/")
async def root():
    return {"message": "Hello World"}





    # cursor.execute("""INSERT INTO posts(title,content) VALUES(%s,%s) RETURNING *""",(new_post.title,new_post.content))
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"Post": new_post}
    # post_dict = new_post.dict()
    # post_dict["id"] = randrange(0, 1000000)
    # # print(f"New post Title: {new_post.title}, Content: {new_post.content}, Published: {new_post.published}, Rating: {new_post.rating}")
    # my_posts.append(post_dict)
    # # raise HTTPException(status_code=status.HTTP_201_CREATED, detail=f"Post created successfully with id {post_dict['id']}")


