import logging
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select

from services.wildberries import Wildberries
from db.session_maker import session_manager
from v1.products.models import Product

logger = logging.getLogger(__name__)
wb = Wildberries()


async def add_product_to_db(
        session, data: dict, auto_update: bool
):
    """
    Создает в БД продукт.
    :param session: Текущая сессия.
    :param data: Новые данные.
    :param auto_update: Значение продукта насчет автообновления
    :return: Возврат созданного продукта
    """
    product = Product(
        artikul=data.get("id"),
        name=data.get("name"),
        price=data.get("salePriceU"),
        rating=data.get("rating"),
        quantity=data.get("totalQuantity"),
        auto_update=auto_update
    )
    session.add(product)
    return product


async def update_product_to_db(
        session, product_exist: Product, new_data: dict, auto_update: bool
):
    """
    Обновляет существующий продукт.
    :param session: Текущая сессия.
    :param product_exist: Объект сущ. продукта
    :param new_data: Новые данные.
    :param auto_update: Значение продукта насчет автообновления
    :return: Возврат обновленного продукта
    """
    product_exist.name = new_data.get("name")
    product_exist.price = new_data.get("salePriceU")
    product_exist.rating = new_data.get("rating")
    product_exist.quantity = new_data.get("totalQuantity")
    product_exist.updated_at = datetime.now()
    product_exist.auto_update = auto_update
    session.add(product_exist)
    return product_exist


@session_manager.connection(commit=True)
async def add_or_update_product_to_db(session, artikul: int, auto_update: bool):
    """Создает или если существует такой объект с таким артикулом в БД, то
    обновляет/изменяет его на свежие данные"""
    data = await wb.get_detail_product_by_artikul(artikul)
    if data.get("error"):
        raise HTTPException(status_code=404, detail=data.get("error"))

    query = select(Product).where(Product.artikul == artikul)
    result = await session.execute(query)
    product_exist = result.scalars().first()

    if product_exist is None:
        product = await add_product_to_db(
            session=session,
            data=data,
            auto_update=auto_update
        )
    else:
        product = await update_product_to_db(
            session=session,
            product_exist=product_exist,
            new_data=data,
            auto_update=auto_update
        )

    return product


async def get_all_auto_update_products(session):
    """ Получить все объекты у которых флаг 'auto_update' """
    query = select(Product).where(Product.auto_update == True)
    result = await session.execute(query)
    products = result.scalars().all()
    return products


@session_manager.connection(commit=True)
async def upd_all_auto_up_products_to_db(session):
    """ Автоматическое обновление всех продуктов с флагом 'auto_update' """
    all_products = await get_all_auto_update_products(session=session)
    if all_products:
        for product in all_products:
            new_data = await wb.get_detail_product_by_artikul(product.artikul)

            await update_product_to_db(
                session=session,
                product_exist=product,
                new_data=new_data,
                auto_update=True
            )
        logger.info("Scheduler - Updated data")
    else:
        logger.info("No data available")




