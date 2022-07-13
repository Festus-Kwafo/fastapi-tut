from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'data': {'name': 'Susan'}}

@app.get('/blog/{id}')
def get_blog(id: int):
    return {'data': id}