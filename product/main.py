from fastapi import FastAPI
from . import models
from .database import engine
from .routers import product, seller, login


app = FastAPI(
    title="Products API",
    description="All products related info",
    contact={
        "Developer name": "Shah Rahman",
    },
    docs_url="/documentation",
)
models.Base.metadata.create_all(bind=engine)

app.include_router(product.router)

app.include_router(seller.router)

app.include_router(login.router)
