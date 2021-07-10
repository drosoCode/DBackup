import os
import shutil


def backup(address: str, port: int, user: str, password: str, database: str, out: str):
    if port is None:
        port = 8088
    os.system(f"influxd backup -portable -host {address}:{port} -db {database} {out}")