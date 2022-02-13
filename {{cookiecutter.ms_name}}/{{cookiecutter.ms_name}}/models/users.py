# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import event, text

from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, EmailStr
from typing import Optional, List

# from {{cookiecutter.ms_name}}.ext.database import async_session


class TokenStr(BaseModel):
    username: Optional[str] = None


class ModelUserUpdate(SQLModel):
    name: str = Field("Complet name", min_length=10, nullable=False)
    email: EmailStr
    username: str = Field("", index=True, min_length=4)
    enable: bool = Field(default=True)
    rule_id: int = Field(default=None, foreign_key="rules.id", gt=0)


class ModelUserBase(SQLModel):
    name: str = Field("Complet name", min_length=10, nullable=False)
    email: EmailStr
    username: str = Field("", index=True, min_length=4)
    enable: bool = Field(default=True)
    rule_id: int = Field(default=None, foreign_key="rules.id", gt=0)
    password: str = Field("password", min_length=6, nullable=False)


class ModelUser(ModelUserBase, table=True):
    __tablename__ = "user"
    id: int = Field(default=None, primary_key=True)
    rule: Optional["ModelRules"] = Relationship(back_populates="user")
    created_at: datetime = Field(default=datetime.now())


class ModelRules(SQLModel, table=True):
    __tablename__ = "rules"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=40)
    role: str = Field(max_length=40)
    user: List[ModelUser] = Relationship(back_populates="rule")


class BlackListToken(SQLModel, table=True):
    __tablename__ = "blacklist"
    id: int | None = Field(None, primary_key=True)
    token: str


# @event.listens_for(ModelRules.__table__, "after_create")
# def create_fist_user(target, connection=async_session().connection(), **kwargs):

#     roles = [
#         {
#             "name": "User",
#             "role": "role:user"
#         },
#         {
#             "name": "Administrador",
#             "role": "role:admin"
#         }
#     ]

#     for role in roles:
#         connection.execute(text(
#             'INSERT INTO "rules" (name, role) '
#             f"VALUES ('{role.get('name')}', '{role.get('role')}')"))
