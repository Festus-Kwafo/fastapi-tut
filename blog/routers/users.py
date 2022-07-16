from blog.schemas import BaseUserSchema, UserSchema
from fastapi import APIRouter, Depends, status
from blog.database import get_db
from sqlalchemy.orm import Session
from ..repository import users

router = APIRouter(
    prefix= '/user',
    tags=['User']
)


@router.post('',  status_code=status.HTTP_201_CREATED, response_model=BaseUserSchema)
def user(request: UserSchema, db: Session = Depends(get_db)):
    return users.create(request, db)


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=BaseUserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return users.get(user_id, db)
