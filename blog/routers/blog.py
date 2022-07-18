from typing import List
from blog.schemas import ShowBlogSchema, BlogSchema

from fastapi import APIRouter, Depends, status
from blog.database import some_engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from ..repository import blog
from blog.oauth import get_current_user
from blog.schemas import UserSchema
router = APIRouter(
    prefix="/blog",
    tags=['Blog']
)

@router.get('', status_code=status.HTTP_200_OK, response_model=List[ShowBlogSchema], )
def get_blog(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    return blog.get_all(db)

@router.post('', status_code=status.HTTP_201_CREATED, )
def create_blog(request: BlogSchema, db: Session = Depends(get_db)):
    return blog.create(request, db )


@router.get('/{blog_id}', status_code=status.HTTP_200_OK, response_model=ShowBlogSchema, )
def get_single_blog(blog_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    return blog.get_single(blog_id, db)


@router.delete('/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    return blog.delete(blog_id, db)


@router.put('/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id: int, request: BlogSchema, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    return blog.update(blog_id, request, db)
