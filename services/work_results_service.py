from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import WorkResult, Order

class WorkResultRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, order_id: int, status: str, worker: Optional[str] = None, inspector: Optional[str] = None) -> WorkResult:
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise ValueError(f"Order {order_id} not found")

        work_result = WorkResult(
            order_id=order_id,
            status=status,
            worker=worker,
            inspector=inspector
        )
        try:
            self.db.add(work_result)
            self.db.commit()
            self.db.refresh(work_result)
            return work_result
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_by_id(self, work_result_id: int) -> Optional[WorkResult]:
        return self.db.query(WorkResult).filter(WorkResult.id == work_result_id).first()

    def get_all(self) -> List[WorkResult]:
        return self.db.query(WorkResult).all()

    def get_by_order_id(self, order_id: int) -> List[WorkResult]:
        return self.db.query(WorkResult).filter(WorkResult.order_id == order_id).all()

    def update(self, work_result_id: int, status: Optional[str] = None, 
              worker: Optional[str] = None, inspector: Optional[str] = None) -> Optional[WorkResult]:
        work_result = self.get_by_id(work_result_id)
        if not work_result:
            return None

        try:
            if status is not None:
                work_result.status = status
            if worker is not None:
                work_result.worker = worker
            if inspector is not None:
                work_result.inspector = inspector
            self.db.commit()
            self.db.refresh(work_result)
            return work_result
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete(self, work_result_id: int) -> bool:
        work_result = self.get_by_id(work_result_id)
        if not work_result:
            return False

        try:
            self.db.delete(work_result)
            self.db.commit()
            return True
        except SQLAlchemyError:
            self.db.rollback()
            raise

# Service functions
def create_work_result(db: Session, order_id: int, status: str, 
                      worker: Optional[str] = None, inspector: Optional[str] = None) -> WorkResult:
    repo = WorkResultRepository(db)
    return repo.create(order_id, status, worker, inspector)

def get_work_result(db: Session, work_result_id: int) -> Optional[WorkResult]:
    repo = WorkResultRepository(db)
    return repo.get_by_id(work_result_id)

def get_all_work_results(db: Session) -> List[WorkResult]:
    repo = WorkResultRepository(db)
    return repo.get_all()

def get_work_results_by_order(db: Session, order_id: int) -> List[WorkResult]:
    repo = WorkResultRepository(db)
    return repo.get_by_order_id(order_id)

def update_work_result(db: Session, work_result_id: int, 
                      status: Optional[str] = None,
                      worker: Optional[str] = None,
                      inspector: Optional[str] = None) -> Optional[WorkResult]:
    repo = WorkResultRepository(db)
    return repo.update(work_result_id, status=status, worker=worker, inspector=inspector)

def delete_work_result(db: Session, work_result_id: int) -> bool:
    repo = WorkResultRepository(db)
    return repo.delete(work_result_id)