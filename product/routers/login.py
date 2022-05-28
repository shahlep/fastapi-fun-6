from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext

router = APIRouter(
    tags=['login'],
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.Seller).filter(
        models.Seller.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Username not found!')
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Invalid password!')
    return request
