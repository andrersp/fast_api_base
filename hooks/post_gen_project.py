import os
import shutil
from venv import EnvBuilder
import secrets
from secrets import token_hex


def remove(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
    elif os.path.isdir(filepath):
        shutil.rmtree(filepath)


with open(".gitignore", "a+") as file:
    file.write("\n.env")
    file.write("\n.settings.toml")

with open(".env", "a+") as file:

    token_key = token_hex(32)
    file.write(f'\nSECRET_KEY= "{token_key}"')
