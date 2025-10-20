from sqlalchemy.orm import Session
from models import Order

def create_order(db, order_name, product_code):
    new_order = Order(order_name=order_name, product_code=product_code)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

def get_all_orders(db):
    return db.query(Order).all()

