from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

router = APIRouter(
    tags=["login"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Generate with running openssl rand -hex 32 in terminal
SECRET_KEY = "fcc1d1ad94cf1318bef217dd3469b869c3553a310d0ba8eb65a53201d92a9871"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20


def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(get_db)):
    seller = (
        db.query(models.Seller)
            .filter(models.Seller.username == request.username)
            .first()
    )
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Username not found!"
        )
    if not pwd_context.verify(request.password, seller.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password!"
        )
    access_token = generate_token(
        data={'user': seller.username}
    )
    return {'access_token':access_token,'token_type':'bearer'}
