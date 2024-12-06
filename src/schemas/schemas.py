from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class ProductBase(BaseModel):
    name: str
    category: str
    price: float
    stock: int


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True



class InventoryLogBase(BaseModel):
    product_id: int
    quantity: int
    operation_type: str 
    date: datetime


class InventoryLogCreate(InventoryLogBase):
    pass


class InventoryLogResponse(InventoryLogBase):
    id: int

    class Config:
        orm_mode = True



class MonthlyReport(BaseModel):
    product_name: str
    total_quantity: int
    operation_type: str


class YearlyReport(BaseModel):
    product_name: str
    total_quantity: int
    operation_type: str
