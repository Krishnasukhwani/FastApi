from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import schemas, database, oauth2
from typing import List
from ..repository import blog

router = APIRouter(
    tags=['blogs'],
    prefix="/blog"
)
get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED )
async def create_blog(request: schemas.Blog, db: Session = Depends(get_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
    return blog.create(request,db)

@router.get('/', response_model=List[schemas.ShowBlog])
async def get_all(db: Session = Depends(get_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)

@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
async def show(id, db: Session = Depends(get_db),current_user:schemas.User = Depends(oauth2.get_current_user) ):
    return blog.get_one(id, db)
    


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id, db: Session = Depends(get_db),current_user:schemas.User = Depends(oauth2.get_current_user) ):
    return blog.destroy(id, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowBlog)
async def update_blog(id, request:schemas.Blog, db: Session = Depends(get_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
   return blog.update(id,request, db)