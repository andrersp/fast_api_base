# -*- coding: utf-8 -*-
from typing import List

from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from sqlalchemy import and_, asc, or_
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext

from {{cookiecutter.ms_name}}.models.users import ModelUser, ModelUserBase, ModelUserUpdate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_passowod, hashed_password):
    return pwd_context.verify(plain_passowod, hashed_password)


def get_password_hashed(plain_passowod):
    return pwd_context.hash(plain_passowod)


async def authenticate_user(username: str, password: str, session: AsyncSession):

    query = (
        select(ModelUser)
        .where(ModelUser.username == username)
        .options(selectinload(ModelUser.rule))
    )
    user = await session.execute(query)
    result = user.scalar()

    if result:
        if not verify_password(password, result.password):
            return False
        return result
    return False


async def verify_username(username: str, email: str, session: AsyncSession):

    query = select(ModelUser).where(
        or_(ModelUser.username == username, ModelUser.email == email)
    )
    user = await session.execute(query)
    return user.scalar()


async def get_active_user(username: str, session: AsyncSession):

    query = (
        select(ModelUser)
        .filter_by(username=username)
        .options(selectinload(ModelUser.rule))
    )
    user = await session.execute(query)
    result = user.scalar()
    if result:
        return _serialize_user(result)
    return False


async def create_user_db(user_data: ModelUserBase, session: AsyncSession):

    user_data.password = get_password_hashed(user_data.password)
    user = ModelUser(**user_data.dict())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(id_user: int, data: ModelUserUpdate, session: AsyncSession):

    user = await session.get(ModelUser, id_user)
    if not user:
        return False
    user.email = data.email
    user.username = data.username
    user.name = data.name
    user.rule_id = data.rule_id
    user.enable = data.enable
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_all_users(skip: int, limit: int, session: AsyncSession):

    skip = skip * limit

    query = (
        select(ModelUser)
        .options(selectinload(ModelUser.rule))
        .offset(skip)
        .limit(limit)
        .order_by(asc(ModelUser.id))
    )

    result = await session.execute(query)
    users = result.scalars()
    return _serialize_users(users) if users else False


async def select_user(user_id: int, session: AsyncSession):

    query = (
        select(ModelUser)
        .where(ModelUser.id == user_id)
        .options(selectinload(ModelUser.rule))
    )
    query = await session.execute(query)
    user = query.scalar()
    return _serialize_user(user) if user else False


async def change_status(user_id: int, register_id: int):

    async with async_session() as session:
        query = select(ModelUser).where(
            and_(ModelUser.cg_id == register_id, ModelUser.id == user_id)
        )

        user = await session.execute(query)
        user = user.scalar()

        if user:

            user.enable = False if user.enable else True
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    return False


def _serialize_users(users: List[ModelUser]):

    return list(
        map(
            lambda x: {
                "id": x.id,
                "username": x.username,
                "email": x.email,
                "enable": x.enable,
                "rule": {"id": x.rule.id, "name": x.rule.name} if x.rule_id else False,
            },
            users,
        )
    )


def _serialize_user(user):

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "enable": user.enable,
        "rule": {"id": user.rule.id, "name": user.rule.name} if user.rule_id else False,
    }
