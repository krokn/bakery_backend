from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import user
from src.user.utils_registration import decoded


def get_user(refresh_token: str, session: Session):
    data = decoded(refresh_token)
    logger.info(f'data: {data}')
    name = data['name']
    logger.info(f'name: {name}')
    core_query = select(user).where(user.c.name == name)
    result = session.execute(core_query)
    core_row = result.fetchone()
    return core_row