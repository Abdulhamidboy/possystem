from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.base.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

    logs = relationship("InventoryLog", back_populates="product")


class InventoryLog(Base):
    __tablename__ = "inventory_logs"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    operation_type = Column(String(20), nullable=False) 
    date = Column(DateTime, default=func.now(), nullable=False)

    product = relationship("Product", back_populates="logs")

    __table_args__ = (
        CheckConstraint("operation_type IN ('in', 'out')", name="check_operation_type"),
    )
