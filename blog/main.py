from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException

from . import models, schemas, hashing
from .database import engine, SessionLocal
from sqlalchemy.orm import Session


models.Base.metadata.create_all(engine)
app = FastAPI()


@app.get('/')
def index():
    return {'data': {'name': 'Susan'}}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBLog])
def get_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{blog_id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBLog)
def get_single_blog(blog_id: int, response: Response, db: Session = Depends(get_db)):
    single_blog = db.query(models.Blog).filter(
        models.Blog.id == blog_id).first()
    if not single_blog:
        raise HTTPException(status_code=404, detail="Item not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"data": f"This blog with id {blog_id} does not exist"}

    return single_blog


@app.delete('/blog/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Item not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "data"


@app.put('/blog/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Item not found")
    blog.update(request, synchronize_session=False)
    db.commit()
    return "Updated Successfully"




@app.post('/user',  status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


