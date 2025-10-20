from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from models import Order

class OrderRepository:
    """Repository for Order persistence operations (create, list, update status)."""
    def __init__(self, db: Session):
        self.db = db

    def create(self, order_name: str, product_code: str) -> Order:
        new_order = Order(order_name=order_name, product_code=product_code)
        try:
            self.db.add(new_order)
            self.db.commit()
            self.db.refresh(new_order)
            return new_order
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_all(self) -> List[Order]:
        return self.db.query(Order).all()

    def update_status(self, order_id: int, status: str) -> Optional[Order]:
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return None
        try:
            order.status = status
            self.db.commit()
            self.db.refresh(order)
            return order
        except SQLAlchemyError:
            self.db.rollback()
            raise

# Service functions delegate to OrderRepository

def create_order(db: Session, order_name: str, product_code: str) -> Order:
    repo = OrderRepository(db)
    return repo.create(order_name, product_code)

def get_all_orders(db: Session) -> List[Order]:
    repo = OrderRepository(db)
    return repo.get_all()

def update_order_status(db: Session, order_id: int, status: str) -> Optional[Order]:
    repo = OrderRepository(db)
    return repo.update_status(order_id, status)
