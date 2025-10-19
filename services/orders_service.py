from sqlalchemy.orm import Session
from models import Order

def create_order(db: Session, order_name: str, product_code: str):
    new_order = Order(order_name=order_name, product_code=product_code)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

def get_all_orders(db: Session):
    return db.query(Order).all()

