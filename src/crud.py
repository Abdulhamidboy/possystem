from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from fastapi import HTTPException
import src.models
import src.schemas.schemas as schemas


async def get_products(db: AsyncSession):
    result = await db.execute(select(src.models.Product))
    return result.scalars().all()


async def get_product_by_id(db: AsyncSession, product_id: int):
    result = await db.execute(select(src.models.Product).filter(src.models.Product.id == product_id))
    return result.scalars().first()


async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    db_product = src.models.Product(
        name=product.name,
        category=product.category,
        price=product.price,
        stock=product.stock
    )
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def update_product(db: AsyncSession, product_id: int, updated_product: schemas.ProductCreate):
    result = await db.execute(select(src.models.Product).filter(src.models.Product.id == product_id))
    db_product = result.scalars().first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name = updated_product.name
    db_product.category = updated_product.category
    db_product.price = updated_product.price
    db_product.stock = updated_product.stock
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def delete_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(src.models.Product).filter(src.models.Product.id == product_id))
    db_product = result.scalars().first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.delete(db_product)
    await db.commit()
    return db_product


async def get_inventory_logs(db: AsyncSession):
    result = await db.execute(select(src.models.InventoryLog))
    return result.scalars().all()


async def get_inventory_log_by_id(db: AsyncSession, log_id: int):
    result = await db.execute(select(src.models.InventoryLog).filter(src.models.InventoryLog.id == log_id))
    return result.scalars().first()


async def create_inventory_log(db: AsyncSession, log: schemas.InventoryLogCreate):
    result = await db.execute(select(src.models.Product).filter(src.models.Product.id == log.product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if log.operation_type == "out" and product.stock < log.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    if log.operation_type == "in":
        product.stock += log.quantity
    elif log.operation_type == "out":
        product.stock -= log.quantity

    db_log = src.models.InventoryLog(
        product_id=log.product_id,
        quantity=log.quantity,
        operation_type=log.operation_type,
    )
    db.add(db_log)
    await db.commit()
    await db.refresh(db_log)
    return db_log


async def delete_inventory_log(db: AsyncSession, log_id: int):
    result = await db.execute(select(src.models.InventoryLog).filter(src.models.InventoryLog.id == log_id))
    db_log = result.scalars().first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    await db.delete(db_log)
    await db.commit()
    return db_log


async def get_report(db: AsyncSession, year: int, month: int = None):
    query = (
        select(
            src.models.Product.name,
            func.sum(src.models.InventoryLog.quantity).label("total_quantity"),
            src.models.InventoryLog.operation_type
        )
        .join(src.models.InventoryLog, src.models.Product.id == src.models.InventoryLog.product_id)
        .filter(func.extract("year", src.models.InventoryLog.date) == year)
    )
    if month:
        query = query.filter(func.extract("month", src.models.InventoryLog.date) == month)

    result = await db.execute(query.group_by(src.models.Product.name, src.models.InventoryLog.operation_type))
    return result.all()


async def get_monthly_report(db: AsyncSession, year: int, month: int):
    return await get_report(db, year, month)


async def get_yearly_report(db: AsyncSession, year: int):
    return await get_report(db, year)
