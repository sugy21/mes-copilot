from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from database import get_db
from services import orders_service

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(
    order_name: str,
    product_code: str,
    db: Session = Depends(get_db)
):
    """Create a new order"""
    try:
        return orders_service.create_order(db, order_name, product_code)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order"
        )

@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get a specific order by ID"""
    order = orders_service.get_order(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found"
        )
    return order

@router.get("/")
def list_orders(db: Session = Depends(get_db)):
    """Get all orders"""
    try:
        return orders_service.get_all_orders(db)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve orders"
        )

@router.put("/{order_id}")
def update_order(
    order_id: int,
    order_name: Optional[str] = None,
    product_code: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Update a specific order"""
    try:
        order = orders_service.update_order(
            db, order_id, order_name, product_code
        )
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order {order_id} not found"
            )
        return order
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update order"
        )

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete a specific order"""
    try:
        if not orders_service.delete_order(db, order_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order {order_id} not found"
            )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete order"
        )