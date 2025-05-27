from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.cart import CartItem, CartItemCreate
from app.services.cart import get_cart_items, add_to_cart, remove_from_cart
from app.core.security import oauth2_scheme

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/", response_model=List[CartItem])
def view_cart(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    # In a real app, you would get user_id from the token
    # For simplicity, we'll use a hardcoded user_id
    user_id = 1
    return get_cart_items(db, user_id=user_id)

@router.post("/", response_model=CartItem, status_code=201)
def add_item_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user_id = 1
    return add_to_cart(db, user_id=user_id, cart_item=item)

@router.delete("/{item_id}")
def remove_item_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user_id = 1
    success = remove_from_cart(db, cart_item_id=item_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    return {"message": "Item removed from cart"}