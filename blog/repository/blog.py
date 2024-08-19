from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models, schemas

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def get_one(id:int,db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail:f"Blog with id {id} not exist"'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not exist")
    return blog

def create(blog: schemas.Blog,  db:Session):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id =1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id:int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    blog.delete(synchronize_session=False)
    db.commit()
    return "Blog deleted Successfully!"


def update(id:int, blog: schemas.Blog,  db:Session ):
    updated_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not updated_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} not found!")
    if blog.title:
        updated_blog.title =blog.title
    if blog.body:
        updated_blog.body = blog.body
    db.commit()
    return f"updated blog: {updated_blog}"