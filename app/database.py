from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Connect to the postgres database

# while(True):
    
#     try:
#         conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='FastApi', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("database connected")
#         break
#     except Exception as e:
#         print("database not connected");
#         print("Error :", e)
#         time.sleep(2)        

# my_posts = [{"title": "title of post 1", "content": "content of post 1", "published": True, "rating": 5, "id": 1}, 
#             {"title": "title of post 2", "content": "content of post 2", "published": True, "rating": 4, "id": 2}]

