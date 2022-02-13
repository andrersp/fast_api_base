# -*- coding: utf-8 -*-

from fastapi import Depends
from fastapi_permissions import (
    Allow,
    Authenticated,
    Deny,
    Everyone,
    configure_permissions,
    All,
)

from {{cookiecutter.ms_name}}.core.auth import get_current_role
from {{cookiecutter.ms_name}}.models.users import ModelUser
from {{cookiecutter.ms_name}}.ext.exceptions import CustomException


acl_roles = [
    (Allow, Authenticated, "view"),
    (Allow, "role:dev", All),
    (Allow, "role:admin", "admin"),
    (Allow, "role:admin", "operator"),
    (Allow, "role:admin", "client"),
    (Allow, "role:operational", "operator"),
    (Allow, "role:client", "client"),
]


def get_user_role(role: ModelUser = Depends(get_current_role)):

    if role:
        # user is logged in
        principals = [Everyone, Authenticated]
        principals.append(role)
    else:
        # user is not logged in
        principals = [Everyone]

    return principals


role_exception = CustomException(
    status_code=403, message=[{"type": "permissao", "msg": "Permissão insuficiente"}]
)

Permission = configure_permissions(get_user_role, role_exception)
