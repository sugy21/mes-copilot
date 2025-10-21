from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from database import get_db
from services import work_results_service
from schemas import WorkResultCreate, WorkResultUpdate, WorkResultResponse

router = APIRouter(prefix="/work-results", tags=["work_results"])

@router.post("/", response_model=WorkResultResponse, status_code=status.HTTP_201_CREATED)
def create_work_result(
    work_result: WorkResultCreate,
    db: Session = Depends(get_db)
):
    """Create a new work result"""
    try:
        return work_results_service.create_work_result(
            db=db,
            order_id=work_result.order_id,
            status=work_result.status,
            worker=work_result.worker,
            inspector=work_result.inspector
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )

@router.get("/{work_result_id}", response_model=WorkResultResponse)
def get_work_result(work_result_id: int, db: Session = Depends(get_db)):
    """Get a specific work result by ID"""
    result = work_results_service.get_work_result(db, work_result_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work result {work_result_id} not found"
        )
    return result

@router.get("/", response_model=List[WorkResultResponse])
def list_work_results(db: Session = Depends(get_db)):
    """Get all work results"""
    return work_results_service.get_all_work_results(db)

@router.get("/order/{order_id}", response_model=List[WorkResultResponse])
def list_work_results_by_order(order_id: int, db: Session = Depends(get_db)):
    """Get all work results for a specific order"""
    return work_results_service.get_work_results_by_order(db, order_id)

@router.put("/{work_result_id}", response_model=WorkResultResponse)
def update_work_result(
    work_result_id: int,
    work_result: WorkResultUpdate,
    db: Session = Depends(get_db)
):
    """Update a specific work result"""
    result = work_results_service.update_work_result(
        db,
        work_result_id,
        status=work_result.status,
        worker=work_result.worker,
        inspector=work_result.inspector
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work result {work_result_id} not found"
        )
    return result

@router.delete("/{work_result_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_work_result(work_result_id: int, db: Session = Depends(get_db)):
    """Delete a specific work result"""
    if not work_results_service.delete_work_result(db, work_result_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work result {work_result_id} not found"
        )