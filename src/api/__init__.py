from fastapi import APIRouter
from .inventory import router as inventory_router
from .products import router as products_router
from .reports import router as reports_router

router = APIRouter()

router.include_router(inventory_router)
router.include_router(products_router)
router.include_router(reports_router)

__all__ = ["inventory_router", "products_router", "reports_router"]
