from fastapi import FastAPI, Depends, status, Response, HTTPException
from  . import models, schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List





app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED )
def ceate(blog:schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, response_model=schemas.ShowBlog)
def delete_blog(id, db: Session = Depends(get_db) ):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    blog.delete(synchronize_session=False)
    db.commit()
    return "Blog deleted Successfully!"

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowBlog)
async def update_blog(id, blog:schemas.Blog, db: Session = Depends(get_db)):
    updated_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not updated_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} not found!")
    if blog.title:
        updated_blog.title =blog.title
    if blog.body:
        updated_blog.body = blog.body
    db.commit()
    return f"updated blog: {updated_blog}"
    

@app.get('/blog', response_model=List[schemas.ShowBlog])
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id, response:Response, db: Session = Depends(get_db) ):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail:f"Blog with id {id} not exist"'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not exist")
    return blog
