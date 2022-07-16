from fastapi import FastAPI
from . import models
from .database import engine
from blog.routers import blog, users, authentication


models.Base.metadata.create_all(engine)
app = FastAPI()



@app.get('/')
def index():
    return {'data': {'name': 'Susan'}}
    
app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(users.router)


