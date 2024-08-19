from ..hashing import Hash
from .. import schemas, database, models
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


def create(user:  schemas.User, db: Session):
    hashed_password= Hash.bcrypt(user.password)
    new_user = models.User(name=user.name, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_one(id:int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not exist")
    return user