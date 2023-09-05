from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from typing import Optional, Union, List

from app import oauth2
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)



# def find_post(id):
#     for post in my_posts:
#         if post["id"] == id:
#             return post
        

# def find_post_index(id):
#     for index, post in enumerate(my_posts):
#         if post["id"] == id:
#             return index

# @router.get("/")
# async def root():
#     return {"message": "Hello World"}


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.email)
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

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post  = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
    
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error": "post not found"}
    return post


@router.delete("/{id}", response_model=schemas.Post)
def delete_post(id: int, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
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


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post_from_db = post_query.first()
    
    if post_from_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
        
    post_query.update(post.dict(), synchronize_session=False)
    
    db.commit()
    
    return post_query.first()