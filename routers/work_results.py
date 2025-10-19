from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services import work_results_service

router = APIRouter(prefix="/results", tags=["work_results"])

@router.post("/")
def create_result(order_id: int, status: str, worker: str, db: Session = Depends(get_db)):
    # Copilot 실습 포인트: 오류 유발, 디버깅, 리팩토링
    return work_results_service.create_result(db, order_id, status, worker)

