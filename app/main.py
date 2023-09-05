import datetime
from typing import Optional, Union, List
from webbrowser import get
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth
models.Base.metadata.create_all(bind=engine)

app = FastAPI()




# Connect to the postgres database

while(True):
    
    try:
        conn = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='FastApi', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connected")
        break
    except Exception as e:
        print("database not connected");
        print("Error :", e)
        time.sleep(2)        

my_posts = [{"title": "title of post 1", "content": "content of post 1", "published": True, "rating": 5, "id": 1}, 
            {"title": "title of post 2", "content": "content of post 2", "published": True, "rating": 4, "id": 2}]




app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)