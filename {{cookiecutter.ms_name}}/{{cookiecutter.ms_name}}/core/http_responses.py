# -*- coding: utf-8 -*-
from typing import List
from fastapi.responses import JSONResponse

from {{cookiecutter.ms_name}}.ext.exceptions import CustomException


response_schema = {
    201: {
        "description": "Send Report",
        "content": {"application/json": {"example": {"success": True}}},
    }
}

ERROR_500 = [{"type": "internal_error", "msg": "Internal error"}]


def success(params: dict = {}, status_code: int = 200):

    response = params.copy()

    response.update({"success": True})

    return JSONResponse(status_code=status_code, content=response)


def error(params: List[dict] = [], status_code: int = 422):
    """TODO:
    model = [
        {
            "msg": "Número de CPF/CNPJ inválido.",
            "type": "value_error"
        }

    ]
    """
    if status_code == 500 and not params:
        params = ERROR_500

    response = {"success": False}
    response.update({"detail": params})

    return JSONResponse(status_code=status_code, content=response)
