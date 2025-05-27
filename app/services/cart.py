from typing import List

from sqlalchemy.orm import Session

from app.models.cart import CartItem
from app.schemas.cart import CartItemCreate

def get_cart_items(db: Session, user_id: int) -> List[CartItem]:
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()

def add_to_cart(db: Session, user_id: int, cart_item: CartItemCreate) -> CartItem:
    db_cart_item = CartItem(**cart_item.model_dump(), user_id=user_id)
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

def remove_from_cart(db: Session, cart_item_id: int, user_id: int) -> bool:
    db_cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.user_id == user_id
    ).first()
    if db_cart_item:
        db.delete(db_cart_item)
        db.commit()
        return True
    return False