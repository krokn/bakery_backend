from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import product


def get_product(session: Session):
    query = select(product)
    result = session.execute(query)
    data = result.all()
    session.commit()
    products = [{"id": product[0],
                 "name": product[1],
                 "price": float(product[2]),  # Преобразуем Decimal в float для JSON-сериализации
                 "imageUrl": product[3]} for product in data]
    return products


def get_product_name(session: Session):
    query = select(product).order_by(product.c.name.asc())
    result = session.execute(query)
    data = result.all()
    session.commit()
    products = [{"id": product[0],
                 "name": product[1],
                 "price": float(product[2]),  # Преобразуем Decimal в float для JSON-сериализации
                 "imageUrl": product[3]} for product in data]
    return products


def get_product_up(session: Session):
    query = select(product).order_by(product.c.price.asc())
    result = session.execute(query)
    data = result.all()
    session.commit()
    products = [{"id": product[0],
                 "name": product[1],
                 "price": float(product[2]),  # Преобразуем Decimal в float для JSON-сериализации
                 "imageUrl": product[3]} for product in data]
    return products


def get_product_down(session: Session):
    query = select(product).order_by(product.c.price.desc())
    result = session.execute(query)
    data = result.all()
    session.commit()
    products = [{"id": product[0],
                 "name": product[1],
                 "price": float(product[2]),  # Преобразуем Decimal в float для JSON-сериализации
                 "imageUrl": product[3]} for product in data]
    return products