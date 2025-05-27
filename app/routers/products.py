from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.product import Product, ProductCreate
from app.services.product import (
    get_products, get_product, create_product, 
    update_product, delete_product
)
from app.core.security import oauth2_scheme
from app.services.user import get_user_by_email

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = get_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_new_product(
    product: ProductCreate, 
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    # In a real app, you would verify the token and check if user is admin
    # For simplicity, we'll just check if the token exists
    return create_product(db=db, product=product)

@router.put("/{product_id}", response_model=Product)
def update_existing_product(
    product_id: int, 
    product: ProductCreate, 
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    db_product = update_product(db=db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}")
def delete_existing_product(
    product_id: int, 
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    success = delete_product(db=db, product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}