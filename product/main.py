from fastapi import FastAPI, Depends, status, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/product", status_code=status.HTTP_201_CREATED)
def add(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name, description=request.description, price=request.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@app.get(
    "/products",
    response_model=List[schemas.DisplayProduct],
    status_code=status.HTTP_200_OK,
)
def get_all_product(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@app.get(
    "/products/{id}",
    response_model=schemas.DisplayProduct,
    status_code=status.HTTP_200_OK,
)
def get_product_by_id(id, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!"
        )
    return product


@app.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def get_product_to_delete(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(
        synchronize_session=False
    )
    db.commit()
    return f"product entry remove from db as requested!"


@app.put("/product/{id}", status_code=status.HTTP_200_OK)
def update_product_by_id(
        id: int, request: schemas.Product, db: Session = Depends(get_db)
):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found!"
        )
    else:
        product.update(request.dict())
        db.commit()
        return f"Product successfully updated!"


@app.post('/seller')
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    new_seller = models.Seller(username=request.username,
                               email=request.email, password=request.password)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)

    return new_seller
