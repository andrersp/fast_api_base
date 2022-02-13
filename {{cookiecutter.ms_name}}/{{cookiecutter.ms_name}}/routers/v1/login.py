# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm


from {{cookiecutter.ms_name}}.core import auth
from {{cookiecutter.ms_name}}.core.http_responses import error, success
from {{cookiecutter.ms_name}}.utils import default_messages
from {{cookiecutter.ms_name}}.ext.database import get_session
from {{cookiecutter.ms_name}}.crud.users import authenticate_user


router = APIRouter(tags=["Login"])


@router.post("/login", summary="Login endpoint")
async def login_for_access_user(
    form_data: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)
):

    user = await authenticate_user(form_data.username, form_data.password, session)

    if not user:
        return error(
            default_messages.make_response(
                "login", "Nome de usuário ou senha incorreta"
            ),
            422,
        )

    if not user.enable:
        return error(
            default_messages.make_response(
                "login", "Usuário não habilitado."), 403
        )

    access_token = auth.create_access_token(
        data={
            "sub": user.username,
            "id": user.id,
            "email": user.email,
            "role": user.rule.role if user.rule_id else "",
        }
    )

    data = {
        "access_token": access_token,
        "token_type": "bearer",
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "rule": {"id": user.rule_id, "rule_name": user.rule.name}
        if user.rule_id
        else "",
        "name": user.name,
    }

    return success(data)
