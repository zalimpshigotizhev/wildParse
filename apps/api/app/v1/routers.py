
from fastapi import APIRouter, HTTPException

from v1.logic.scheduler.db import add_or_update_product_to_db, upd_all_auto_up_products_to_db
from v1.products.schemas import (
    ProductItemSchema
)

router = APIRouter()


@router.post("/v1/products")
async def create_products(item: ProductItemSchema):
    new_product = await add_or_update_product_to_db(
        artikul=item.artikul,
        auto_update=False
    )
    return new_product


@router.get("/v1/subscribe/{artikul}")
async def get_subscription(artikul: int):
    new_product = await add_or_update_product_to_db(
        artikul=artikul,
        auto_update=True
    )
    return new_product
