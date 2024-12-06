from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.base.database import get_db
from src.crud import get_monthly_report, get_yearly_report

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/monthly/{year}/{month}")
def fetch_monthly_report(year: int, month: int, db: Session = Depends(get_db)):
    report = get_monthly_report(db, year, month)
    if not report:
        raise HTTPException(status_code=404, detail="No data for the specified period")
    return report


@router.get("/yearly/{year}")
def fetch_yearly_report(year: int, db: Session = Depends(get_db)):
    report = get_yearly_report(db, year)
    if not report:
        raise HTTPException(status_code=404, detail="No data for the specified year")
    return report
