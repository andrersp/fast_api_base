# -*- coding: utf- -*-

from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from os import environ as env


class CustomException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code


async def unicorn_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "errors": exc.message},
    )
