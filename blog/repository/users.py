from blog.schemas import UserSchema, ShowUserSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException
from blog.hashing import Hash
from blog.models import User


def create(request: UserSchema, db: Session):
    new_user = User(name=request.name, email=request.email,
                    password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get(user_id: int, db:Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f'User with id {user_id} does not exist')
    return user
