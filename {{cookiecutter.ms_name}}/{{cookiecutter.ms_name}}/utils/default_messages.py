# -*- coding: utf-8 -*-

MSG_REGISTER_NOT_FOUND = [{"type": "cadastro", "msg": "Registro não encontrado"}]

MSG_CASE_NOT_FOUND = [{"type": "case", "msg": "Caso não encontrado"}]

MSG_DUPLICATE_CASE_CLIENT = [
    {"type": "case_name", "msg": "Já existe um caso com esse nome para esse cliente."}
]
MSG_PRODUCT_NOT_FOUND = [{"type": "produto", "msg": "Produto não encontrado"}]

MSG_CONTEXT_NOT_FOUND = [{"type": "contexto", "msg": "Contexto não encontrado"}]
MSG_DUPLICATE_MAIL = [
    {"type": "register", "msg": "Já existe um cadastro com esse e-mail"}
]
MSG_DUPLICATE_CPF_CNPJ = [
    {"type": "register", "msg": "Já existe um cadastro com esse CPF/CNPJ"}
]

MSG_DUPLICATE_USERNAME = [
    {
        "type": "register",
        "msg": "Já existe um cadastro com esse nome de usuário e/ou email",
    }
]
MSG_ERROR_FOLLOWUP_NO_FOUND = [{"type": "register", "msg": "Seguimento não encontrado"}]
MSG_ERROR_POSITION_NOT_FOUND = [{"type": "register", "msg": "Posição não encontrado"}]
MSG_ERROR_OFFICE_NOT_FOUND = [{"type": "register", "msg": "Cargo encontrado"}]


def make_response(msg_type: str, msg: str):
    return [{"type": f"{msg_type}", "msg": f"{msg}"}]


MSG_TARGET_EXISTS = [
    {"type": "target", "msg": "Já existe um target com esse CPF/CNPJ nesse caso."}
]
