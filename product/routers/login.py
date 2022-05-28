from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext

router = APIRouter(
    tags=['login'],
)


@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(get_db)):
    return request
