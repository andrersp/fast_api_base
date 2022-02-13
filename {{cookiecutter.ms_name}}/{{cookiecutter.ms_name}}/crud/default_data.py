# -*- coding: utf-8 -*-

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
from datetime import datetime

from {{cookiecutter.ms_name}}.models.users import ModelUser, ModelRules
from {{cookiecutter.ms_name}}.crud.users import get_password_hashed


async def create_default_rules(conn: AsyncSession):
    roles = [
        {"name": "Administrator", "role": "role:admin"},
        {"name": "Developer", "role": "role:dev"},
    ]

    for role in roles:
        query = select(ModelRules).where(ModelRules.role == role.get("role"))
        user = await conn.execute(query)
        result = user.scalar()

        if not result:
            await conn.execute(
                text(
                    'INSERT INTO "rules" (name, role) '
                    f"VALUES ('{role.get('name')}', '{role.get('role')}')"
                )
            )


async def create_first_user(conn: AsyncSession):
    query = select(ModelUser).where(ModelUser.username == "admin")
    user = await conn.execute(query)
    result = user.scalar()

    if not result:
        user = ModelUser(
            name="admin",
            username="admin",
            email="email@mail.com",
            rule_id=1,
            enable=True,
            password=get_password_hashed("admin"),
        )
        password = get_password_hashed("admin")
        await conn.execute(
            text(
                'INSERT INTO "user" (name, email, username, enable, rule_id, password, created_at) '
                f"VALUES ('administrador', 'email@mail.com', 'admin',True, 1, '{password}', '{datetime.now()}')"
            )
        )
