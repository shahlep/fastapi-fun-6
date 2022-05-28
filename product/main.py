from fastapi import FastAPI, Depends, status, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .routers import product,seller


app = FastAPI(
    title='Products API',
    description='All products related info',
    contact={
        "Developer name":"Shah Rahman",
    },
    docs_url='/documentation'
)
models.Base.metadata.create_all(bind=engine)

app.include_router(product.router)

app.include_router(seller.router)

