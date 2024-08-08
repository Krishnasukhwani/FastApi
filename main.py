from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app =FastAPI()

class Blog(BaseModel):
    title:str
    body:str
    published_at: Optional[bool]

@app.get('/')
def index():
    return {'data': 'blog list'}

@app.get('/blog/{id}')
def about(id: int):
    return {'data': id}

@app.post('blog')
def create_blog(blog:Blog):
    return {'data':f"Blog is created with title as {blog.title}"}


# if __name__ =="__main__":
#     import uvicorn
#     uvicorn.run(app, host="localhost", port=9000)
