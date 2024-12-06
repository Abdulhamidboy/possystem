from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
import src.models
import src.schemas.schemas as schemas


def get_products(db: Session):
    return db.query(src.models.Product).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(src.models.Product).filter(src.models.Product.id == product_id).first()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = src.models.Product(
        name=product.name,
        category=product.category,
        price=product.price,
        stock=product.stock
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, updated_product: schemas.ProductCreate):
    db_product = db.query(src.models.Product).filter(src.models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name = updated_product.name
    db_product.category = updated_product.category
    db_product.price = updated_product.price
    db_product.stock = updated_product.stock
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(src.models.Product).filter(src.models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return db_product



def get_inventory_logs(db: Session):
    return db.query(src.models.InventoryLog).all()


def get_inventory_log_by_id(db: Session, log_id: int):
    return db.query(src.models.InventoryLog).filter(src.models.InventoryLog.id == log_id).first()


def create_inventory_log(db: Session, log: schemas.InventoryLogCreate):
    product = db.query(src.models.Product).filter(src.models.Product.id == log.product_id).first()
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
    db.commit()
    db.refresh(db_log)
    return db_log


def delete_inventory_log(db: Session, log_id: int):
    db_log = db.query(src.models.InventoryLog).filter(src.models.InventoryLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    db.delete(db_log)
    db.commit()
    return db_log


def get_report(db: Session, year: int, month: int = None):
    query = (
        db.query(
            src.models.Product.name,
            func.sum(src.models.InventoryLog.quantity).label("total_quantity"),
            src.models.InventoryLog.operation_type
        )
        .join(src.models.InventoryLog, src.models.Product.id == src.models.InventoryLog.product_id)
        .filter(func.extract("year", src.models.InventoryLog.date) == year)
    )
    if month:
        query = query.filter(func.extract("month", src.models.InventoryLog.date) == month)
    
    return query.group_by(src.models.Product.name, src.models.InventoryLog.operation_type).all()


def get_monthly_report(db: Session, year: int, month: int):
    return get_report(db, year, month)


def get_yearly_report(db: Session, year: int):
    return get_report(db, year)
