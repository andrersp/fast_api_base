# -*- coding: utf-8 -*-

from fastapi import FastAPI
from {{cookiecutter.ms_name}}.routers.v1.login import router as login_router
from {{cookiecutter.ms_name}}.routers.v1.user import router as user_router


def init_app(app: FastAPI):
    app.include_router(login_router, prefix="/v1")
    app.include_router(user_router, prefix="/v1")
    pass
    # app.include_router(report_router, prefix="/v1")
