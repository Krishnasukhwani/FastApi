from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import schemas, database
from ..repository import user
from .. import oauth2

router = APIRouter(
    tags=['users'],
    prefix="/user"
)
get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
async def create_user(request: schemas.User, db: Session = Depends(get_db),current_user:schemas.User = Depends(oauth2.get_current_user)):
    return user.create(request, db)
    

@router.get('/',response_model=schemas.ShowUser)
async def get_user(id:int, db: Session=Depends(get_db), current_user:schemas.User = Depends(oauth2.get_current_user)):
    return user.get_one(id, db)