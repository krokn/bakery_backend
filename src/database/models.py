from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, TIMESTAMP, String, ForeignKey, func, Boolean, UniqueConstraint, \
    Numeric, DateTime

metadata = MetaData()

product = Table(
    "product",
    metadata,
    Column(
        "id",
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    ),
    Column("name", String, nullable=False),
    Column("price", Numeric, nullable=False),
    Column("imageUrl", String, nullable=False),
)

user = Table(
    "user",
    metadata,
    Column(
        "id",
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    ),
    Column("name", String, nullable=False, unique=True),
    Column("password", String, nullable=False),
)

orders = Table(
    "orders",
    metadata,
    Column(
        "id",
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    ),
    Column("user_id", Integer, ForeignKey('user.id'), nullable=False),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("total_price", Numeric),
)


order_items = Table(
    "order_items",
    metadata,
    Column(
        "id",
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    ),
    Column("order_id", Integer, ForeignKey('orders.id'), nullable=False),
    Column("product_id", Integer, ForeignKey('product.id'), nullable=False),
    Column("quantity", Integer, nullable=False),
)


