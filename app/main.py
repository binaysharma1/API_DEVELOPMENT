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
from fastapi import Depends

from . import models,schemas
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine) #this will create the tables in the database if they don't exist already

app=FastAPI()




    
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


@app.post("/posts/create", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post = models.Post(title=new_post.title, content=new_post.content)
    db.add(post)
    db.commit()
    db.refresh(post)
    return  post



    # cursor.execute("""INSERT INTO posts(title,content) VALUES(%s,%s) RETURNING *""",(new_post.title,new_post.content))
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"Post": new_post}
    # post_dict = new_post.dict()
    # post_dict["id"] = randrange(0, 1000000)
    # # print(f"New post Title: {new_post.title}, Content: {new_post.content}, Published: {new_post.published}, Rating: {new_post.rating}")
    # my_posts.append(post_dict)
    # # raise HTTPException(status_code=status.HTTP_201_CREATED, detail=f"Post created successfully with id {post_dict['id']}")





@app.get("/posts",response_model=list[schemas.Post])

def test_posts(db: Session = Depends(get_db)):
        posts = db.query(models.Post).all()

    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
        return posts






@app.get("/posts/{id}",response_model=schemas.Post)
def get_post_by_id(id: int,response:Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    # post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return  post
    # # for post in my_posts:
    #     if post["id"] == id:
    # #         return {"Post": post}
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
       








@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    db.delete(post)
    db.commit()
    return {"message": f"Post with id {id} deleted successfully"}

@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    post.title = updated_post.title
    post.content = updated_post.content
    post.published = updated_post.published
    db.commit()
    db.refresh(post)
    return post

    # for index, post in enumerate(my_posts):
    #     if post["id"] == id:
    #         my_posts[index] = updated_post.dict()
    #         my_posts[index]["id"] = id  # Ensure the ID remains the same
    #         return {"message": f"Post with id {id} updated successfully", "post": my_posts[index]}
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")


    return {"message": f"Post with id {id} updated successfully", "post": updated_post_data}
    
    # for index, post in enumerate(my_posts):
    #     if post["id"] == id:
    #         my_posts[index] = updated_post.dict()
    #         my_posts[index]["id"] = id  # Ensure the ID remains the same
    #         return {"message": f"Post with id {id} updated successfully", "post": my_posts[index]}
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")




#code for user operations

@app.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.LoginResponse)
def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(models.User).filter(models.User.email == new_user.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {new_user.email} already exists")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while checking for existing user")
    user = models.User(email=new_user.email, password=new_user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully"}


#in login, first email uniqueness is tested then asked for password then user login successful
@app.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.LoginResponse)
def login_user(user_credentials: schemas.UserAuth, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {user_credentials.email} not found")
    if user.password != user_credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    return {"message":"User Login successful"}
