
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db



router = APIRouter(
    prefix="/api/v1/user",
)


#in login, first email uniqueness is tested then asked for password then user login successful
@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.LoginResponse)
def login_user(user_credentials: schemas.UserAuth, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {user_credentials.email} not found")
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    return {"message":"User Login successful"}



#code for user operations

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.LoginResponse)
def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == new_user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {new_user.email} already exists")

    hashed_password = utils.hash_password(new_user.password)
    user = models.User(email=new_user.email, password=hashed_password)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A user with this email already exists")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create user")
    db.refresh(user)
    return {"message": "User created successfully"}



#Get user 
@router.get("/{id}",response_model=schemas.UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user
