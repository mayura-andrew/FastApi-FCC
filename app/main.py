import datetime
from typing import Optional, Union, List
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from passlib.context import CryptContext 
from . import models, schemas
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
        

def find_post_index(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index

@app.get("/")
async def root():
    print(my_posts)
    return {"message": "Hello World"}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


# @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
#     # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,  (post.title, post.content, post.published))
#     # new_post = cursor.fetchone()
#     # conn.commit()
    
#     # new_post = models.Post(title=post.title, content=post.content, published=post.published)
#     new_post = models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return {"data": "post created successfully", "post": new_post}
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# @app.post("/createpost")
# def create_posts(post: schemas.Post):
#     print(post.dict())
#     return {"data": post}

# @app.get("/posts/latest")
# def get_latest_posts():
#     post = my_posts[len(my_posts)-1]
#     return{"post details": post}

@app.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post  = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
    
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error": "post not found"}
    return post


@app.delete("/posts/{id}", response_model=schemas.Post)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # delete_post = cursor.fetchone()
    # conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id == id )
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post_from_db = post_query.first()
    
    if post_from_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
        
    post_query.update(post.dict(), synchronize_session=False)
    
    db.commit()
    
    return post_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
