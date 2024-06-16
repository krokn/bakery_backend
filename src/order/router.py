from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Header
from loguru import logger
from sqlalchemy import insert, select, desc
from sqlalchemy.orm import Session

from src.database.connection import get_sync_session
from src.database.models import orders, order_items, user as UserModels, product
from src.order.shema import OrderCreate
from src.telegram_admin.send import send_telegram_message
from src.user.utils_user import get_user

router = APIRouter(
    prefix="/api/orders",
    tags=["order"]
)

@router.post("/")
def add_order(order_data: OrderCreate, session: Session = Depends(get_sync_session), authorization: str | None = Header(default=None)):
    logger.info(f"refresh_token: {authorization}")
    if authorization is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Нет куки")
    else:
        user = get_user(authorization, session)
        user_id = user[0]
    try:
        stmt = insert(orders).values(user_id=user_id, total_price=order_data.totalPrice)
        result = session.execute(stmt)
        session.flush()
        latest_order_id = result.inserted_primary_key[0]
        for item in order_data.items:
            stmt = insert(order_items).values(order_id=latest_order_id, product_id=item.id, quantity=item.count)
            session.execute(stmt)
        session.commit()
        orders_query = select(orders).order_by(desc(orders.c.created_at)).limit(1)
        result = session.execute(orders_query).fetchone()

        if not result:
            return {"message": "No orders found"}

        order_id = result[0]
        user_id = result[1]
        created_at = result[2]
        total_price = result[3]

        logger.info(f"user_id: {user_id}")

        user_query = select(UserModels).where(UserModels.c.id == user_id)
        logger.info(f"user_query: {user_query}")
        user_result = session.execute(user_query).fetchone()
        logger.info(f"user_result: {user_result}")
        user_name = user_result[1] if user_result else 'Unknown'
        logger.info(f"user_name: {user_name}")

        items_query = select(order_items, product).where(order_items.c.order_id == order_id).where(
            order_items.c.product_id == product.c.id)
        items_result = session.execute(items_query).fetchall()
        items = [{'Название товара': item[5], 'Количество': item[3], 'Цена': item[6]} for item in items_result]

        order_info = {
            'Номер заказа': order_id,
            'Пользователь': user_name,
            'Дата создания': created_at,
            'Общая сумма': total_price,
            'Товары': items
        }
        try:
            message = (
                f"Номер заказа: {order_info['Номер заказа']}\n"
                f"Пользователь: {order_info['Пользователь']}\n"
                f"Дата создания: {order_info['Дата создания'].isoformat()}\n"
                f"Общая сумма: {order_info['Общая сумма']}\n"
                f"Товары:\n"
            )

            for item in order_info['Товары']:
                message += f"- {item['Название товара']} - {item['Количество']} шт. по цене {item['Цена']} руб.\n"

            logger.info(order_info)
            send_telegram_message(message)
        except KeyError as e:
            logger.error(f"KeyError: {e} in order_info: {order_info}")
            return {"error": f"KeyError: {e}"}
        return {"message": "Order created successfully", "order_id": latest_order_id}
    except Exception as e:
        session.rollback()
        raise




