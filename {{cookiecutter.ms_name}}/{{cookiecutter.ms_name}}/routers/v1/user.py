# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Query
from {{cookiecutter.ms_name}}.core.auth import get_current_user

from {{cookiecutter.ms_name}}.core.http_responses import success, error
from {{cookiecutter.ms_name}}.models.users import ModelUser, ModelUserBase, ModelUserUpdate
from {{cookiecutter.ms_name}}.core.access_role import Permission, acl_roles
from {{cookiecutter.ms_name}}.ext.database import get_session
from {{cookiecutter.ms_name}}.crud import users as crud_user
from {{cookiecutter.ms_name}}.utils import default_messages

router = APIRouter(tags=["User"], prefix="/user")


@router.post("", summary="Create new User")
async def create_user(
    data: ModelUserBase,
    acls: list = Permission("admin", acl_roles),
    session=Depends(get_session),
):

    if await crud_user.verify_username(data.username, data.email, session):
        return error(params=default_messages.MSG_DUPLICATE_USERNAME)

    try:
        user = await crud_user.create_user_db(data, session)
    except Exception as err:
        return error(status_code=500)

    return success({"id": user.id}, status_code=201)


@router.get("", summary="List all users")
async def get_all_user(
    page: int = 0,
    limit: int | None = Query(50, le=100),
    acls: list = Permission("admin", acl_roles),
    session=Depends(get_session),
):

    try:
        users = await crud_user.get_all_users(page, limit, session)
    except Exception as exc:
        print(exc)
        return error(status_code=500)
    else:
        return success(params={"data": users})


@router.get("/me", summary="Get My user data")
async def about_me(
    acls: list = Permission("view", acl_roles),
    user: ModelUser = Depends(get_current_user),
):

    return success(user)


@router.get("/{id_user}", summary="Select User by ID")
async def select_user(
    id_user: int,
    acls: list = Permission("admin", acl_roles),
    session=Depends(get_session),
):

    try:
        user = await crud_user.select_user(id_user, session)
    except Exception as exc:
        print(exc)
        return error(status_code=500)

    if not user:
        return error(default_messages.MSG_REGISTER_NOT_FOUND, status_code=404)

    return success(user)


@router.put("/{id_user}", summary="Update user data")
async def update_user(
    id_user: int,
    data: ModelUserUpdate,
    acls: list = Permission("admin", acl_roles),
    session=Depends(get_session),
):

    try:
        user = await crud_user.verify_username(data.username, data.email, session)
    except Exception as exc:
        return error(status_code=500)

    if user and user.id != id_user:
        return error(default_messages.MSG_DUPLICATE_USERNAME)

    try:
        user = await crud_user.update_user(id_user, data, session)
    except:
        return error(status_code=500)

    return success({"id": user.id, "email": user.email})
