# -*- coding: utf-8 -*-

import asyncio
from pycpfcnpj import cpf as cpf_validator
from sentry_sdk import capture_exception

from {{cookiecutter.ms_name}}.core.schemas.report_schema import ReportSchema
from {{cookiecutter.ms_name}}.core.send_report import send_report


async def requester(data: ReportSchema):

    cpf_cnpj = data.cpf_cnpj
    name = data.name
    service_id = data.service_id
    target_id = data.target_id
    webhook = data.webhook

    result = await _make_request(name, cpf_cnpj)

    if result:
        await send_report(service_id, target_id, webhook, result)
        return
    await send_report(service_id, target_id, webhook, {}, False)


async def _make_request(
    name: str, cpf_cnpj: str, attempt: int = 0, max_attemps: int = 10
):

    try:
        print(f"{name} {cpf_cnpj}")

        return {"success": True}

    except Exception as exc:

        if attempt < max_attemps:
            print(f"Tentativa {attempt} de {max_attemps}")
            attempt += 1
            return await _make_request(name, cpf_cnpj, attempt)
        else:
            capture_exception(exc)

    return False
