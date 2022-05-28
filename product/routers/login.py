from fastapi import APIRouter,Depends,HTTPException,status
from .. import schemas,models,database
from sqlalchemy.orm import Session
from passlib.context import CryptContext

router = APIRouter(
    tags=['login'],
)


@router.post('/login')
def login(request:schemas.Login):
    return request
