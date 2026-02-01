
from typing import Optional, List
from fastapi import  status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..db import models
from ..schemas import schemas
from ..db.database import  engine, get_db
from ..base.utils import hash_password

router=APIRouter(prefix='/users', tags=['Users'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def crete_user(user: schemas.UsersCreate, db: Session = Depends(get_db)):
    
    user.password= hash_password(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int,  db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with {id} does not exist')
    return user