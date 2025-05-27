from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.order import Order, OrderCreate
from app.services.order import create_order, get_orders
from app.core.security import oauth2_scheme

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=Order, status_code=201)
def place_order(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user_id = 1
    order = create_order(db, user_id=user_id)
    if not order:
        raise HTTPException(status_code=400, detail="Could not create order")
    return order

@router.get("/", response_model=List[Order])
def view_orders(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user_id = 1
    return get_orders(db, user_id=user_id)