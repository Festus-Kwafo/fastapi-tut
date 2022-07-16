from fastapi import APIRouter, Depends, HTTPException
from blog.hashing import Hash
from blog.schemas import LoginSchema
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from blog.database import get_db
from blog.models import User
from blog.JWTtoken import create_access_token

router = APIRouter(
    tags= ["Authentication"]
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()
    print(user)
    if not user:
        raise HTTPException(
            status_code=404, detail=f'User with username {request.username} does not exist')

    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=404, detail=f'Incorrect Password')
    access_token = create_access_token(
        data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}