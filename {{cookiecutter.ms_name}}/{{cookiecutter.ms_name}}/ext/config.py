# -*- coding: utf-8 -*-
from importlib import import_module
from {{cookiecutter.ms_name}}.ext.settings import settings


def init_app(app):
    app.title = "{{cookiecutter.ms_name}}"
    for extension in settings.EXTENSIONS:
        mod = import_module(extension)
        mod.init_app(app)
