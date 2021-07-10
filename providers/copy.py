import os
import shutil


def backup(address: str, port: int, user: str, password: str, database: str, out: str):
    try:
        shutil.copytree(database, out)
    except NotADirectoryError:
        shutil.copy2(database, out)
