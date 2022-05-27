from fastapi import FastAPI, Depends
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/product")
def add(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name, description=request.description, price=request.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return request


@app.get('/products')
def get_all_product(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@app.get('/products/{id}')
def get_all_product(id, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    return product
