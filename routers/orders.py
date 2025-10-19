from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services import orders_service

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/")
def create_order(order_name: str, product_code: str, db: Session = Depends(get_db)):
    # Copilot 실습 포인트: Docstring 설명, 리팩토링, 예외처리 추가
    return orders_service.create_order(db, order_name, product_code)

@router.get("/")
def get_orders(db: Session = Depends(get_db)):
    return orders_service.get_all_orders(db)

