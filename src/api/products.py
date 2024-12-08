from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.base.database import get_db
from src.crud import (
    get_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product,
)
from src.schemas.schemas import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductResponse])
async def fetch_products(db: AsyncSession = Depends(get_db)):
    return await get_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
async def fetch_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductResponse)
async def add_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await create_product(db, product)


@router.put("/{product_id}", response_model=ProductResponse)
async def modify_product(product_id: int, product: ProductCreate, db: AsyncSession = Depends(get_db)):
    updated_product = await update_product(db, product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@router.delete("/{product_id}", response_model=ProductResponse)
async def remove_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
