# -*- coding: utf-8 -*-

from sqlalchemy import event, text

from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from {{cookiecutter.ms_name}}.ext.settings import settings
from {{cookiecutter.ms_name}}.ext.exceptions import CustomException

from {{cookiecutter.ms_name}}.crud import users as crud_user
from {{cookiecutter.ms_name}}.ext.database import get_session
from {{cookiecutter.ms_name}}.models.users import ModelUser, TokenStr, ModelRules


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login", auto_error=False)


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        hours=int(settings.ACCESS_TOKEN_EXPIRE_HOURS)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


async def get_user(username: str, session):
    user = await crud_user.get_active_user(username, session)
    if user:
        return user


async def get_current_user(
    token: str = Depends(oauth2_scheme), session=Depends(get_session)
):
    error_credential = [{"type": "credential",
                         "msg": "Could not valide credential"}]

    credentials_exception = CustomException(
        status_code=401, message=error_credential)

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        username = payload.get("sub")

        if not username:
            raise credentials_exception

        token_data = TokenStr(username=username)
    except JWTError as e:

        raise credentials_exception

    user = await get_user(username=token_data.username, session=session)

    if not user:
        raise credentials_exception

    if not user["enable"]:
        raise CustomException(
            status_code=400, message=[{"type": "access", "msg": "User not enable"}]
        )
    return user


async def get_current_role(token: str = Depends(oauth2_scheme)):
    error_credential = [{"type": "credential", "msg": "Credencial inválida"}]

    credentials_exception = CustomException(
        status_code=401, message=error_credential)

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        role = payload.get("role")

        if not role:
            raise credentials_exception

    except JWTError as e:

        raise credentials_exception

    else:
        return role
