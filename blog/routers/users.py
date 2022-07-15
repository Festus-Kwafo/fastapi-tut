from typing import List
from blog.schemas import BaseUserSchema, UserSchema
from blog.models import User
from blog.hashing import Hash
from fastapi import APIRouter, Depends, status, HTTPException
from blog.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= '/user',
    tags=['User']

)


@router.post('',  status_code=status.HTTP_201_CREATED, response_model=BaseUserSchema, )
def user(request: UserSchema, db: Session = Depends(get_db)):
    new_user = User(name=request.name, email=request.email,
                    password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=BaseUserSchema, tags=['User'])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f'User with id {user_id} does not exist')
    return user
