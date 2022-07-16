from sqlalchemy.orm import Session
from blog.models import Blog
from fastapi import HTTPException
from blog.schemas import BlogSchema

def get_all(db: Session):
        blogs = db.query(Blog).all()
        return blogs

def create(request: BlogSchema, db: Session,):
    new_blog = Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def get_single(blog_id: int, db: Session):
        single_blog = db.query(Blog).filter(
                Blog.id == blog_id).first()
        if not single_blog:
                raise HTTPException(status_code=404, detail="Item not found")
        return single_blog


def delete(blog_id: int, db: Session):
    blog = db.query(Blog).filter(Blog.id == blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Item not found")
    blog.delete()
    db.commit()
    return "data"

def update(blog_id: int, request: BlogSchema, db: Session):
    blog = db.query(Blog).filter(Blog.id == blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Item not found")
    blog.update(request.dict())
    db.commit()
    return "Updated Successfully"