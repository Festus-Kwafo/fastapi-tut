from typing import List
from blog.schemas import ShowBlogSchema, BlogSchema
from blog.models import Blog
from fastapi import APIRouter, Depends, status, Response, HTTPException
from blog.database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/blog",
    tags=['Blog']
)

@router.get('', status_code=status.HTTP_200_OK, response_model=List[ShowBlogSchema], )
def get_blog(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs

@router.post('', status_code=status.HTTP_201_CREATED, )
def create_blog(blog: BlogSchema, db: Session = Depends(get_db)):
    new_blog = Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/{blog_id}', status_code=status.HTTP_200_OK, response_model=ShowBlogSchema, )
def get_single_blog(blog_id: int, db: Session = Depends(get_db)):
    single_blog = db.query(Blog).filter(
        Blog.id == blog_id).first()
    if not single_blog:
        raise HTTPException(status_code=404, detail="Item not found")
    return single_blog


@router.delete('/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Item not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "data"


@router.put('/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id: int, request: BlogSchema, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Item not found")
    blog.update(request, synchronize_session=False)
    db.commit()
    return "Updated Successfully"
