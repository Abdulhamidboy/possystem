from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.base.database import get_db
from src.crud import get_monthly_report, get_yearly_report

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/monthly/{year}/{month}")
async def fetch_monthly_report(year: int, month: int, db: AsyncSession = Depends(get_db)):
    report = await get_monthly_report(db, year, month)
    if not report:
        raise HTTPException(status_code=404, detail="No data for the specified period")
    return report


@router.get("/yearly/{year}")
async def fetch_yearly_report(year: int, db: AsyncSession = Depends(get_db)):
    report = await get_yearly_report(db, year)
    if not report:
        raise HTTPException(status_code=404, detail="No data for the specified year")
    return report
