from fastapi import APIRouter, HTTPException, status, Depends

# from sqlalchemy.orm import Session
from typing import Dict, Any
from pathlib import Path
import pandas as pd

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/summary", response_model=Dict[str, Any])
def data_summary():
    """
    Read data.csv from project root and return sums of 'quantity' and 'price'.
    """
    project_root = Path(__file__).resolve().parents[1]
    csv_path = project_root / "data.csv"

    if not csv_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="data.csv not found"
        )

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read CSV: {e}",
        )

    missing = [c for c in ("quantity", "price") if c not in df.columns]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required columns: {', '.join(missing)}",
        )

    try:
        qty_sum = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).sum()
        price_sum = pd.to_numeric(df["price"], errors="coerce").fillna(0).sum()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compute sums: {e}",
        )

    return {
        "quantity_sum": int(qty_sum) if float(qty_sum).is_integer() else float(qty_sum),
        "price_sum": (
            int(price_sum) if float(price_sum).is_integer() else float(price_sum)
        ),
        "rows": len(df),
    }
