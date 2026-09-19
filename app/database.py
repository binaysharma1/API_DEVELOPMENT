from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:funk@localhost/db_1"
engine = create_engine(SQLALCHEMY_DATABASE_URL) #engine connects alchemy to database and execute commands

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #it is used to create session

Base = declarative_base() #base helps to create models and tables in the database.



#dependency :it make database session available to the path operation function and close it after the request is completed.
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

