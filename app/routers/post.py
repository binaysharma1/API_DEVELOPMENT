
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from .. import models, schemas,oauth2
from ..database import get_db


router = APIRouter(
    prefix="/api/v1/posts",
    # prefix="/posts"+id doing this, we can remove all posts from the path and just use /{id} for the post id
    tags=["Posts"]
)


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    post = models.Post(
        title=new_post.title,
        content=new_post.content,
        published=new_post.published,
        owner_id=current_user.id,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return  post



@router.get("/{id}",response_model=schemas.Post)
def get_post_by_id(id: int, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    # post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return  post
    # # for post in my_posts:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwiZXhwIjoxNzkwMjUxODYxfQ.P2ZJL6DfNygp7vkEfpX5axjnjy1s3Y2AAGG4QEGZzHs
    #     if post["id"] == id:
    # #         return {"Post": post}
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
       

@router.get("/",response_model=list[schemas.Post], status_code=status.HTTP_200_OK)

def test_posts(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)
,limit:int=10, skip=0, search: str = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    return posts
 

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this post")
    db.delete(post)
    db.commit()
    return {"message": f"Post with id {id} deleted successfully"}



@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this post")
    post.title = updated_post.title
    post.content = updated_post.content
    post.published = updated_post.published
    db.commit()
    db.refresh(post)
    return post


