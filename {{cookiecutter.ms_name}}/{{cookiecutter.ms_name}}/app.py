# -*- coding: utf-8 -*-
from fastapi import FastAPI


from .ext.exceptions import unicorn_exception_handler, CustomException
from .ext import config


def minimal_app():
    app = FastAPI(docs_url="/v1/docs")
    app.add_exception_handler(CustomException, unicorn_exception_handler)
    return app


def create_app():
    app = minimal_app()
    config.init_app(app)
    return app
