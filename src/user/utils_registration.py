import hashlib
import re

import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from config import SECRET_FOR_JWT
from src.database.models import user


def validate_password(password: str):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
    return bool(re.match(pattern, password))


def hashed_password(password):
    password_bytes = password.encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(password_bytes)
    hashed_password = sha256.hexdigest()
    return hashed_password


def identification(name: str, session: Session):
    core_query = select(user).where(user.c.name == name)
    result = session.execute(core_query)
    core_row = result.fetchone()
    return core_row



def authentication(name: str, password: str, session: Session):
    password = hashed_password(password)
    core_row = identification(name, session)
    if core_row.password == password:
        return True
    else:
        return False


def encoded(name: str):
    encoded_jwt = jwt.encode({"name": name}, SECRET_FOR_JWT, algorithm="HS256")
    return encoded_jwt


def decoded(encoded_jwt: str):
    decoded_jwt = jwt.decode(encoded_jwt, SECRET_FOR_JWT, algorithms=["HS256"])
    return decoded_jwt

