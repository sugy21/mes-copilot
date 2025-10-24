from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Order


class OrderRepository:
    """Repository for Order persistence operations"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, order_name: str, product_code: str) -> Order:
        order = Order(order_name=order_name, product_code=product_code)
        try:
            self.db.add(order)
            self.db.commit()
            self.db.refresh(order)
            return order
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_by_id(self, order_id: int) -> Optional[Order]:
        return self.db.query(Order).filter(Order.id == order_id).first()

    def get_all(self) -> List[Order]:
        return self.db.query(Order).all()

    def update(
        self,
        order_id: int,
        order_name: Optional[str] = None,
        product_code: Optional[str] = None,
    ) -> Optional[Order]:
        order = self.get_by_id(order_id)
        if not order:
            return None
        try:
            if order_name is not None:
                order.order_name = order_name
            if product_code is not None:
                order.product_code = product_code
            self.db.commit()
            self.db.refresh(order)
            return order
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete(self, order_id: int) -> bool:
        order = self.get_by_id(order_id)
        if not order:
            return False
        try:
            self.db.delete(order)
            self.db.commit()
            return True
        except SQLAlchemyError:
            self.db.rollback()
            raise


# Service functions
def create_order(db: Session, order_name: str, product_code: str) -> Order:
    repo = OrderRepository(db)
    return repo.create(order_name, product_code)


def get_order(db: Session, order_id: int) -> Optional[Order]:
    repo = OrderRepository(db)
    return repo.get_by_id(order_id)


def get_all_orders(db: Session) -> List[Order]:
    repo = OrderRepository(db)
    return repo.get_all()


def update_order(
    db: Session,
    order_id: int,
    order_name: Optional[str] = None,
    product_code: Optional[str] = None,
) -> Optional[Order]:
    repo = OrderRepository(db)
    return repo.update(order_id, order_name, product_code)


def delete_order(db: Session, order_id: int) -> bool:
    repo = OrderRepository(db)
    return repo.delete(order_id)
