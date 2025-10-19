from sqlalchemy.orm import Session
from models import WorkResult

def create_result(db: Session, order_id: int, status: str, worker: str):
    result = WorkResult(order_id=order_id, status=status, worker=worker)
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
