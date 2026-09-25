from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import psycopg2

from psycopg2.extras import RealDictCursor
import time 

from .config import settings

SQLALCHEMY_DATABASE_URL = settings.database_url
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



    
# while True:  
#     try:
#         conn=psycopg2.connect(host='localhost',database='db_1',user='postgres',password='funk',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Database connection was successful")
#         break;
#     except Exception as error:
#         print("Database connection failed")
#         print("Error:",error)
#         time.sleep(2)
