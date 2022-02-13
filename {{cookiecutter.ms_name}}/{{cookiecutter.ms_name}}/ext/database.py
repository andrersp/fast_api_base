# -*- coding: utf-8 -*-

from fastapi import FastAPI
import os

from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from {{cookiecutter.ms_name}}.ext.settings import settings

from {{cookiecutter.ms_name}}.crud.default_data import create_first_user, create_default_rules


engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        await create_default_rules(conn)
        await create_first_user(conn)


def init_app(app: FastAPI):
    app.add_event_handler("startup", init_db)
    # app.add_event_handler('shutdown', shutdown)
