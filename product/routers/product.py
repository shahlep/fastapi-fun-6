from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import engine, SessionLocal, get_db
from typing import List
from .login import get_current_user

router = APIRouter(
    tags=["Products"],
    prefix="/product",
)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.DisplayProduct
)
def add(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name,
        description=request.description,
        price=request.price,
        seller_id=1,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get(
    "/",
    response_model=List[schemas.DisplayProduct],
    status_code=status.HTTP_200_OK,
)
def get_all_product(db: Session = Depends(get_db),current_user:schemas.Seller=Depends(get_current_user)):
    products = db.query(models.Product).all()
    return products


@router.get(
    "/{id}",
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def get_product_to_delete(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(
        synchronize_session=False
    )
    db.commit()
    return f"product entry remove from db as requested!"


@router.put("/{id}", status_code=status.HTTP_200_OK)
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
