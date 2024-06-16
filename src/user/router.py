from http import HTTPStatus
from loguru import logger

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy import insert
from sqlalchemy.orm import Session
from starlette.responses import Response

from src.database.connection import get_sync_session
from src.database.models import user as UserDatabase
from src.user.shema import User as UserShema
from src.user.utils_registration import validate_password, hashed_password, identification, authentication, encoded
from src.user.utils_user import get_user

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)


@router.post("/register/")
def add_user(user: UserShema, session: Session = Depends(get_sync_session)):
    name, password = user.name, user.password
    if not validate_password(password):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='невалидный пароль')
    else:
        stmt = insert(UserDatabase).values(name=name, password=hashed_password(password))
        session.execute(stmt)
        session.commit()
        raise HTTPException(status_code=HTTPStatus.OK, detail="Пользователь добавлен")


@router.post("/signin")
def signin(user: UserShema, session: Session = Depends(get_sync_session)):
    name, password = user.name, user.password
    logger.info(f"Поступил запрос на вход {name}")
    logger.info(f"Его пароль {password}")
    if identification(name, session) is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Пользователь не найден")
    if authentication(name, password, session) is False:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Неправильный пароль")
    else:
        refresh_token = encoded(name)
        response = Response()
        response.set_cookie(key="refresh_token", value=refresh_token, max_age=86400)
        logger.info(f"Пользователь {name} авторизовался")
        return refresh_token


@router.post("/profile")
def profile(session: Session = Depends(get_sync_session), authorization: str | None = Header(default=None)):
    logger.info(f"refresh_token: {authorization}")
    if authorization is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Нет куки")
    else:
        user = get_user(authorization, session)
        logger.info(f"user: {user}")
        return user[1]
