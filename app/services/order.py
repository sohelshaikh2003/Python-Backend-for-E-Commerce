from typing import List

from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderItemCreate

def create_order(db: Session, user_id: int) -> Order:
    # Get cart items
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    
    if not cart_items:
        return None
    
    # Calculate total and prepare order items
    total = 0.0
    order_items = []
    
    for cart_item in cart_items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if not product or product.stock < cart_item.quantity:
            return None
        
        item_price = product.price * cart_item.quantity
        total += item_price
        
        order_items.append(OrderItemCreate(
            product_id=product.id,
            quantity=cart_item.quantity,
            price=product.price
        ))
    
    # Create order
    db_order = Order(user_id=user_id, total=total)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Create order items and update product stock
    for order_item in order_items:
        db_order_item = OrderItem(**order_item.model_dump(), order_id=db_order.id)
        db.add(db_order_item)
        
        product = db.query(Product).filter(Product.id == order_item.product_id).first()
        product.stock -= order_item.quantity
    
    # Clear cart
    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    
    db.commit()
    return db_order

def get_orders(db: Session, user_id: int) -> List[Order]:
    return db.query(Order).filter(Order.user_id == user_id).all()