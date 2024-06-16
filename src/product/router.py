from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from loguru import logger

from src.database.connection import get_sync_session
from src.product.repository import get_product, get_product_up, get_product_down, get_product_name

router = APIRouter(
    prefix="/api/product",
    tags=["product"]
)


@router.get('')
def get_all_product(
        sortBy: str = Query(None),
        title: str = Query(None),
        session: Session = Depends(get_sync_session)
) -> List[dict]:
    logger.info(f'title = {title}')

    # Получаем продукты с учетом сортировки
    if sortBy is None:
        products = get_product(session)
    elif sortBy in ['title', 'name']:
        products = get_product_name(session)
    elif sortBy == 'price':
        products = get_product_up(session)
    elif sortBy == '-price':
        products = get_product_down(session)
    else:
        products = get_product(session)

    if title:
        products = [product for product in products if title in product['name']]

    return products
