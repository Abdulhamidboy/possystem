from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.base.database import get_db
from src.crud import (
    get_inventory_logs,
    get_inventory_log_by_id,
    create_inventory_log,
    delete_inventory_log,
)
from src.schemas.schemas import InventoryLogCreate, InventoryLogResponse

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/", response_model=list[InventoryLogResponse])
async def fetch_inventory_logs(db: AsyncSession = Depends(get_db)):
    return await get_inventory_logs(db)


@router.get("/{log_id}", response_model=InventoryLogResponse)
async def fetch_inventory_log(log_id: int, db: AsyncSession = Depends(get_db)):
    log = await get_inventory_log_by_id(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Inventory log not found")
    return log


@router.post("/", response_model=InventoryLogResponse)
async def add_inventory_log(log: InventoryLogCreate, db: AsyncSession = Depends(get_db)):
    return await create_inventory_log(db, log)


@router.delete("/{log_id}", response_model=InventoryLogResponse)
async def remove_inventory_log(log_id: int, db: AsyncSession = Depends(get_db)):
    log = await delete_inventory_log(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Inventory log not found")
    return log
